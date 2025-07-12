# Configure the Google Cloud Provider
terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Create a public storage bucket
resource "google_storage_bucket" "public_bucket" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = true

  # Enable uniform bucket-level access
  uniform_bucket_level_access = true

  # Configure CORS for web access
  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["*"]
    max_age_seconds = 3600
  }

  # Configure website settings (optional)
  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }

  # Prevent accidental deletion in production
  lifecycle {
    prevent_destroy = false
  }
}

# Make the bucket publicly readable
resource "google_storage_bucket_iam_member" "public_read" {
  bucket = google_storage_bucket.public_bucket.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

# Create a sample object in the bucket
resource "google_storage_bucket_object" "sample_file" {
  name   = "sample.txt"
  bucket = google_storage_bucket.public_bucket.name
  source = "sample.txt"

  depends_on = [google_storage_bucket.public_bucket]
}

# Generate a random password for the database
resource "random_password" "db_password" {
  length  = 16
  special = true
}

# Create a Cloud SQL PostgreSQL instance
resource "google_sql_database_instance" "postgres_instance" {
  name             = var.db_instance_name
  database_version = var.db_version
  region           = var.region
  deletion_protection = false

  settings {
    tier = var.db_tier
    
    disk_size    = var.db_disk_size
    disk_type    = "PD_SSD"
    disk_autoresize = true
    disk_autoresize_limit = 100

    backup_configuration {
      enabled                        = true
      start_time                     = "02:00"
      location                       = var.region
      point_in_time_recovery_enabled = true
      transaction_log_retention_days = 7
      backup_retention_settings {
        retained_backups = 7
        retention_unit   = "COUNT"
      }
    }

    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "allow-all"
        value = "0.0.0.0/0"
      }
    }

    database_flags {
      name  = "log_statement"
      value = "all"
    }
  }
}

# Create the application database
resource "google_sql_database" "app_database" {
  name     = var.db_name
  instance = google_sql_database_instance.postgres_instance.name
}

# Create a database user
resource "google_sql_user" "db_user" {
  name     = var.db_user
  instance = google_sql_database_instance.postgres_instance.name
  password = random_password.db_password.result
}

# Create Artifact Registry repository for container images
resource "google_artifact_registry_repository" "container_registry" {
  location      = var.region
  repository_id = var.registry_name
  description   = "Container registry for application images"
  format        = "DOCKER"

  docker_config {
    immutable_tags = false
  }

  cleanup_policies {
    id     = "delete-old-images"
    action = "DELETE"
    
    condition {
      tag_state  = "UNTAGGED"
      older_than = "2592000s" # 30 days
    }
  }

  cleanup_policies {
    id     = "keep-minimum-versions"
    action = "KEEP"
    
    most_recent_versions {
      keep_count = var.registry_keep_count
    }
  }
}

# IAM binding for the registry - allow project members to push/pull
resource "google_artifact_registry_repository_iam_member" "registry_admin" {
  project    = var.project_id
  location   = google_artifact_registry_repository.container_registry.location
  repository = google_artifact_registry_repository.container_registry.name
  role       = "roles/artifactregistry.admin"
  member     = "serviceAccount:${var.project_id}@appspot.gserviceaccount.com"
}

# Optional: Create a service account for CI/CD pipeline
resource "google_service_account" "registry_service_account" {
  account_id   = var.registry_service_account_name
  display_name = "Container Registry Service Account"
  description  = "Service account for pushing images to container registry"
}

# Grant the service account permission to push to the registry
resource "google_artifact_registry_repository_iam_member" "registry_writer" {
  project    = var.project_id
  location   = google_artifact_registry_repository.container_registry.location
  repository = google_artifact_registry_repository.container_registry.name
  role       = "roles/artifactregistry.writer"
  member     = "serviceAccount:${google_service_account.registry_service_account.email}"
}

# Create and download service account key (for CI/CD)
resource "google_service_account_key" "registry_key" {
  service_account_id = google_service_account.registry_service_account.name
  public_key_type    = "TYPE_X509_PEM_FILE"
}
