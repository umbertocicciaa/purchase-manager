# Project configuration
variable "project_id" {
  description = "The GCP project ID"
  type        = string
  default     = "my-gcp-project"
}

variable "region" {
  description = "The GCP region for resources"
  type        = string
  default     = "us-central1"
}

# Bucket configuration
variable "bucket_name" {
  description = "Name of the GCS bucket (must be globally unique)"
  type        = string
  default     = "my-public-bucket-unique-name"
}

variable "bucket_location" {
  description = "Location of the GCS bucket"
  type        = string
  default     = "US"
}

# Database configuration
variable "db_instance_name" {
  description = "Name of the Cloud SQL instance"
  type        = string
  default     = "postgres-instance"
}

variable "db_version" {
  description = "PostgreSQL version"
  type        = string
  default     = "POSTGRES_15"
}

variable "db_tier" {
  description = "Machine type for the database instance"
  type        = string
  default     = "db-f1-micro"
}

variable "db_disk_size" {
  description = "Disk size in GB for the database"
  type        = number
  default     = 20
}

variable "db_name" {
  description = "Name of the application database"
  type        = string
  default     = "app_database"
}

variable "db_user" {
  description = "Database user name"
  type        = string
  default     = "app_user"
}
