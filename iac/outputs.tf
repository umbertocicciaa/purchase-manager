# Output the bucket name
output "bucket_name" {
  description = "Name of the created storage bucket"
  value       = google_storage_bucket.public_bucket.name
}

# Output the bucket URL
output "bucket_url" {
  description = "URL of the storage bucket"
  value       = google_storage_bucket.public_bucket.url
}

# Output the public URL for accessing objects
output "bucket_public_url" {
  description = "Public URL for accessing bucket objects"
  value       = "https://storage.googleapis.com/${google_storage_bucket.public_bucket.name}"
}

# Output the bucket self link
output "bucket_self_link" {
  description = "Self link of the storage bucket"
  value       = google_storage_bucket.public_bucket.self_link
}

# Database outputs
output "db_instance_name" {
  description = "Name of the Cloud SQL instance"
  value       = google_sql_database_instance.postgres_instance.name
}

output "db_connection_name" {
  description = "Connection name for the Cloud SQL instance"
  value       = google_sql_database_instance.postgres_instance.connection_name
}

output "db_public_ip" {
  description = "Public IP address of the Cloud SQL instance"
  value       = google_sql_database_instance.postgres_instance.public_ip_address
}

output "db_private_ip" {
  description = "Private IP address of the Cloud SQL instance"
  value       = google_sql_database_instance.postgres_instance.private_ip_address
}

output "db_name" {
  description = "Name of the application database"
  value       = google_sql_database.app_database.name
}

output "db_user" {
  description = "Database user name"
  value       = google_sql_user.db_user.name
  sensitive   = true
}

output "db_password" {
  description = "Database password"
  value       = random_password.db_password.result
  sensitive   = true
}

output "db_connection_string" {
  description = "Database connection string"
  value       = "postgresql://${google_sql_user.db_user.name}:${random_password.db_password.result}@${google_sql_database_instance.postgres_instance.public_ip_address}:5432/${google_sql_database.app_database.name}"
  sensitive   = true
}

# Container Registry outputs
output "registry_url" {
  description = "URL of the Artifact Registry repository"
  value       = "${google_artifact_registry_repository.container_registry.location}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.container_registry.repository_id}"
}

output "registry_name" {
  description = "Name of the Artifact Registry repository"
  value       = google_artifact_registry_repository.container_registry.repository_id
}

output "registry_location" {
  description = "Location of the Artifact Registry repository"
  value       = google_artifact_registry_repository.container_registry.location
}

output "registry_service_account_email" {
  description = "Email of the service account for registry access"
  value       = google_service_account.registry_service_account.email
}

output "registry_service_account_key" {
  description = "Private key for the registry service account (base64 encoded)"
  value       = google_service_account_key.registry_key.private_key
  sensitive   = true
}
