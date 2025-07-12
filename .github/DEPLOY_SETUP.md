# GitHub Actions Setup Guide

This guide explains how to set up the GitHub Actions workflows for automatic deployment of your frontend and backend Docker images to Google Cloud Platform.

## Prerequisites

1. **GCP Project**: A Google Cloud Project with billing enabled
2. **Terraform**: Applied infrastructure (container registry, database, etc.)
3. **GitHub Repository**: Your code repository on GitHub
4. **Service Account**: GCP service account with appropriate permissions

## Required GitHub Secrets

You need to configure the following secrets in your GitHub repository settings:

### Go to: `Settings > Secrets and variables > Actions > New repository secret`

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `GCP_PROJECT_ID` | Your Google Cloud Project ID | From GCP Console or `gcloud config get-value project` |
| `GCP_REGISTRY_LOCATION` | Registry location (e.g., us-central1) | From your terraform variables |
| `GCP_REGISTRY_NAME` | Container registry name | From terraform output: `terraform output registry_name` |
| `GCP_SA_KEY` | Service account JSON key | From terraform output: `terraform output registry_service_account_key` |
| `DATABASE_URL` | PostgreSQL connection string | From terraform output: `terraform output db_connection_string` |

## Step-by-Step Setup

### 1. Get Service Account Key

```bash
cd iac
terraform output -raw registry_service_account_key | base64 -d > service-account-key.json
```

### 2. Configure GitHub Secrets

```bash
# Get project ID
echo "GCP_PROJECT_ID: $(terraform output -raw project_id)"

# Get registry location
echo "GCP_REGISTRY_LOCATION: $(terraform output -raw registry_location)"

# Get registry name
echo "GCP_REGISTRY_NAME: $(terraform output -raw registry_name)"

# Get database URL
echo "DATABASE_URL: $(terraform output -raw db_connection_string)"

# Service account key (copy the entire JSON content)
cat service-account-key.json
```

### 3. Copy Values to GitHub

1. Go to your GitHub repository
2. Navigate to `Settings > Secrets and variables > Actions`
3. Click `New repository secret`
4. Add each secret with the corresponding value

### 4. Enable Required APIs

Make sure these APIs are enabled in your GCP project:

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### 5. Create Database Secret in Secret Manager (Optional)

For better security, store the database password in Secret Manager:

```bash
# Get the database password
DB_PASSWORD=$(terraform output -raw db_password)

# Create secret in Secret Manager
echo -n "$DB_PASSWORD" | gcloud secrets create db-password --data-file=-

# Grant access to the service account
gcloud secrets add-iam-policy-binding db-password \
    --member="serviceAccount:$(terraform output -raw registry_service_account_email)" \
    --role="roles/secretmanager.secretAccessor"
```

## Workflow Features

### Frontend Workflow (`deploy-frontend.yml`)

- **Triggers**: Push to `frontend/` directory on main/develop branches
- **Builds**: Docker image from `frontend/Dockerfile`
- **Deploys**: To Cloud Run as `frontend-app`
- **Port**: 8501 (Streamlit default)
- **Resources**: 512Mi RAM, 1 CPU

### Backend Workflow (`deploy-backend.yml`)

- **Triggers**: Push to `backend/` directory on main/develop branches
- **Builds**: Docker image from `backend/Dockerfile`
- **Deploys**: To Cloud Run as `backend-api`
- **Port**: 8000 (FastAPI default)
- **Resources**: 1Gi RAM, 1 CPU
- **Health Check**: Validates `/health` endpoint

## Image Tags

Both workflows create two tags for each image:

- `latest`: Always points to the most recent build
- `<commit-sha>`: Specific version for rollbacks

Example:

- `us-central1-docker.pkg.dev/my-project/my-registry/frontend:latest`
- `us-central1-docker.pkg.dev/my-project/my-registry/frontend:a1b2c3d4`

## Deployment URLs

After successful deployment, your services will be available at:

- **Frontend**: `https://frontend-app-<hash>-<region>.a.run.app`
- **Backend**: `https://backend-api-<hash>-<region>.a.run.app`

## Customization

### Environment Variables

Modify the `--set-env-vars` in the workflows to add your environment variables:

```yaml
--set-env-vars="ENVIRONMENT=production,API_URL=https://your-backend-url,DEBUG=false"
```

### Resource Allocation

Adjust memory and CPU limits:

```yaml
--memory 2Gi \
--cpu 2 \
--max-instances 20
```

### Health Checks

Add custom health check endpoints to your applications:

**Frontend (Streamlit)**: Add a simple health check page
**Backend (FastAPI)**: Implement `/health` endpoint

## Troubleshooting

### Common Issues

1. **Permission Denied**: Check service account permissions
2. **Image Not Found**: Verify registry URL and authentication
3. **Deployment Fails**: Check Cloud Run service limits
4. **Health Check Fails**: Ensure your app responds on the correct port

### Debug Commands

```bash
# Check service account permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID

# List images in registry
gcloud artifacts docker images list REGISTRY_URL

# Check Cloud Run services
gcloud run services list

# View service logs
gcloud logs read --service=frontend-app
gcloud logs read --service=backend-api
```

## Security Best Practices

1. **Use Secret Manager**: Store sensitive data in GCP Secret Manager
2. **Limit Service Account Permissions**: Grant only necessary roles
3. **Enable Branch Protection**: Require PR reviews before merging
4. **Use Environment-Specific Deployments**: Separate staging and production
5. **Regular Key Rotation**: Rotate service account keys periodically

## Monitoring

Set up monitoring for your deployed services:

```bash
# Enable monitoring
gcloud services enable monitoring.googleapis.com

# Create uptime checks
gcloud alpha monitoring uptime create-check \
    --display-name="Frontend Health Check" \
    --resource-type="url" \
    --resource-labels="host=your-frontend-url"
```
