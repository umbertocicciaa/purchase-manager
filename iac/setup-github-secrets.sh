#!/bin/bash

# GitHub Secrets Setup Helper Script
# This script helps extract values from Terraform outputs for GitHub Actions

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_section() {
    echo -e "${BLUE}[SECTION]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "main.tf" ]; then
    print_error "This script must be run from the iac directory where main.tf is located"
    exit 1
fi

print_section "🔧 GitHub Actions Secrets Setup Helper"
echo ""

print_info "Extracting values from Terraform outputs..."
echo ""

# Check if terraform state exists
if ! terraform show &>/dev/null; then
    print_error "No Terraform state found. Please run 'terraform apply' first."
    exit 1
fi

print_section "📋 GitHub Repository Secrets"
echo ""
echo "Copy these values to your GitHub repository secrets:"
echo "Go to: Settings > Secrets and variables > Actions > New repository secret"
echo ""

# Get all the required values
print_info "GCP_PROJECT_ID:"
PROJECT_ID=$(terraform output -raw project_id 2>/dev/null || echo "NOT_FOUND")
echo "  Value: $PROJECT_ID"
echo ""

print_info "GCP_REGISTRY_LOCATION:"
REGISTRY_LOCATION=$(terraform output -raw registry_location 2>/dev/null || echo "NOT_FOUND")
echo "  Value: $REGISTRY_LOCATION"
echo ""

print_info "GCP_REGISTRY_NAME:"
REGISTRY_NAME=$(terraform output -raw registry_name 2>/dev/null || echo "NOT_FOUND")
echo "  Value: $REGISTRY_NAME"
echo ""

print_info "DATABASE_URL:"
DATABASE_URL=$(terraform output -raw db_connection_string 2>/dev/null || echo "NOT_FOUND")
echo "  Value: $DATABASE_URL"
echo ""

print_info "GCP_SA_KEY (Service Account JSON Key):"
SA_KEY=$(terraform output -raw registry_service_account_key 2>/dev/null || echo "NOT_FOUND")
if [ "$SA_KEY" != "NOT_FOUND" ]; then
    echo "  Creating temporary file: service-account-key.json"
    echo "$SA_KEY" | base64 -d > service-account-key.json
    echo "  ✅ File created. Copy the entire contents of 'service-account-key.json'"
    echo "  ⚠️  Remember to delete this file after copying: rm service-account-key.json"
else
    echo "  Value: NOT_FOUND"
fi
echo ""

print_section "🚀 Quick Setup Commands"
echo ""
echo "1. Enable required Google Cloud APIs:"
echo "   gcloud services enable cloudbuild.googleapis.com"
echo "   gcloud services enable run.googleapis.com"
echo "   gcloud services enable artifactregistry.googleapis.com"
echo "   gcloud services enable secretmanager.googleapis.com"
echo ""

echo "2. Create database secret in Secret Manager (optional, for better security):"
echo "   DB_PASSWORD=\$(terraform output -raw db_password)"
echo "   echo -n \"\$DB_PASSWORD\" | gcloud secrets create db-password --data-file=-"
echo "   gcloud secrets add-iam-policy-binding db-password \\"
echo "     --member=\"serviceAccount:\$(terraform output -raw registry_service_account_email)\" \\"
echo "     --role=\"roles/secretmanager.secretAccessor\""
echo ""

print_section "📝 GitHub Secrets Summary"
echo ""
echo "Required secrets for GitHub Actions:"
echo "┌─────────────────────────┬─────────────────────────────────────┐"
echo "│ Secret Name             │ Value                               │"
echo "├─────────────────────────┼─────────────────────────────────────┤"
echo "│ GCP_PROJECT_ID          │ $PROJECT_ID"
echo "│ GCP_REGISTRY_LOCATION   │ $REGISTRY_LOCATION"
echo "│ GCP_REGISTRY_NAME       │ $REGISTRY_NAME"
echo "│ GCP_SA_KEY              │ Contents of service-account-key.json │"
echo "│ DATABASE_URL            │ $DATABASE_URL"
echo "└─────────────────────────┴─────────────────────────────────────┘"
echo ""

print_section "🔒 Security Recommendations"
echo ""
echo "1. Delete the service account key file after use:"
echo "   rm service-account-key.json"
echo ""
echo "2. Use environment-specific secrets for staging/production"
echo "3. Regularly rotate service account keys"
echo "4. Enable branch protection rules"
echo "5. Review and limit service account permissions"
echo ""

# Check if any values are missing
MISSING_VALUES=0
for value in "$PROJECT_ID" "$REGISTRY_LOCATION" "$REGISTRY_NAME" "$DATABASE_URL" "$SA_KEY"; do
    if [ "$value" = "NOT_FOUND" ]; then
        MISSING_VALUES=1
    fi
done

if [ $MISSING_VALUES -eq 1 ]; then
    print_warning "Some values could not be retrieved. Make sure Terraform has been applied successfully."
else
    print_info "✅ All values retrieved successfully!"
fi

echo ""
print_info "📖 For detailed setup instructions, see: .github/DEPLOY_SETUP.md"
