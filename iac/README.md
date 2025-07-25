# GCP Infrastructure Terraform Configuration

This Terraform configuration creates:

- A public Google Cloud Storage bucket
- A PostgreSQL database (Cloud SQL)
- A container registry (Artifact Registry)

## Prerequisites

1. **Google Cloud SDK**: Install and configure the Google Cloud SDK
2. **Terraform**: Install Terraform (version >= 1.0)
3. **GCP Project**: Have a GCP project with billing enabled
4. **Authentication**: Authenticate with GCP using one of these methods:
   - Service account key file
   - Application Default Credentials (ADC)
   - Google Cloud Shell

## Setup

1. **Clone and navigate to the directory**:

   ```bash
   cd iac
   ```

2. **Configure variables**:

   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

   Edit `terraform.tfvars` with your actual values:
   - `project_id`: Your GCP project ID
   - `bucket_name`: A globally unique bucket name
   - `db_instance_name`: Name for your PostgreSQL instance
   - `db_name`: Name for your application database
   - `db_user`: Database user name

3. **Authenticate with GCP** (choose one method):

   **Option A: Using gcloud CLI**:

   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   gcloud auth application-default login
   ```

   **Option B: Using service account key**:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
   ```

## Deployment

1. **Initialize Terraform**:

   ```bash
   terraform init
   ```

2. **Plan the deployment**:

   ```bash
   terraform plan
   ```

3. **Apply the configuration**:

   ```bash
   terraform apply
   ```

4. **Confirm the deployment** by typing `yes` when prompted.

## What gets created

- **Public GCS Bucket**: A storage bucket with public read access
- **IAM Policy**: Allows `allUsers` to view objects in the bucket
- **CORS Configuration**: Enables cross-origin requests
- **Sample File**: A sample text file uploaded to the bucket
- **PostgreSQL Database**: Cloud SQL PostgreSQL instance with automatic backups
- **Database User**: Application user with generated password
- **Database**: Application database ready for use
- **Container Registry**: Artifact Registry for storing Docker images
- **Registry Service Account**: Service account for CI/CD pipeline access
- **Cleanup Policies**: Automatic cleanup of old container images

## Accessing your resources

### Storage Bucket

After deployment, you can access files in your bucket using:

```
https://storage.googleapis.com/YOUR_BUCKET_NAME/filename
```

For example, the sample file will be available at:

```
https://storage.googleapis.com/YOUR_BUCKET_NAME/sample.txt
```

### PostgreSQL Database

To connect to your database, use the connection details from the Terraform outputs:

```bash
# View sensitive outputs (database credentials)
terraform output db_password
terraform output db_connection_string

# Connect using psql
psql "postgresql://USERNAME:PASSWORD@PUBLIC_IP:5432/DATABASE_NAME"
```

You can also connect from your applications using the connection string provided in the outputs.

### Container Registry

To use the container registry, first authenticate Docker with Google Cloud:

```bash
# Configure Docker to use gcloud as a credential helper
gcloud auth configure-docker LOCATION-docker.pkg.dev

# Get the registry URL
terraform output registry_url

# Build and tag your image
docker build -t REGISTRY_URL/your-app:latest .

# Push the image
docker push REGISTRY_URL/your-app:latest

# Pull the image
docker pull REGISTRY_URL/your-app:latest
```

For CI/CD pipelines, use the service account key:

```bash
# Get the service account key (base64 encoded)
terraform output registry_service_account_key

# Decode and save to file
echo "$(terraform output -raw registry_service_account_key)" | base64 -d > key.json

# Authenticate using the service account
gcloud auth activate-service-account --key-file=key.json
```

**Helper Script**: A `registry-helper.sh` script is provided for common registry operations:

```bash
# Make the script executable
chmod +x registry-helper.sh

# Build and push an image
./registry-helper.sh build my-app latest

# Pull an image
./registry-helper.sh pull my-app latest

# List all images
./registry-helper.sh list
```

## Cleanup

To destroy all resources:

```bash
terraform destroy
```

## Security Notes

⚠️ **Storage Bucket Warning**: This configuration creates a **public** bucket where anyone can read the files. Do not store sensitive data in this bucket.

⚠️ **Database Warning**: The PostgreSQL instance is configured to allow connections from any IP address (0.0.0.0/0) for development purposes. For production, restrict the `authorized_networks` in `main.tf` to specific IP ranges.

⚠️ **Database Credentials**: Database passwords are auto-generated and stored in Terraform state. Use `terraform output db_password` to retrieve them. Consider using Google Secret Manager for production deployments.

## Customization

You can modify the following in `main.tf`:

**Storage Bucket:**

- Bucket location/region
- CORS settings
- Website configuration
- Additional bucket policies

**PostgreSQL Database:**

- Database version (POSTGRES_13, POSTGRES_14, POSTGRES_15)
- Machine tier (db-f1-micro, db-custom-1-3840, etc.)
- Disk size and type
- Backup retention settings
- Network access restrictions
- Database flags and configuration

**Container Registry:**

- Image retention policies
- Cleanup schedules
- IAM permissions
- Repository format (Docker, Maven, npm, etc.)
- Immutable tags setting
