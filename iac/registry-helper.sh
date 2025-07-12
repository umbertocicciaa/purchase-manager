#!/bin/bash

# Container Registry Helper Script
# This script helps with common container registry operations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Check if terraform is available
if ! command -v terraform &> /dev/null; then
    print_error "Terraform is not installed or not in PATH"
    exit 1
fi

# Check if gcloud is available
if ! command -v gcloud &> /dev/null; then
    print_error "Google Cloud SDK is not installed or not in PATH"
    exit 1
fi

# Check if docker is available
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed or not in PATH"
    exit 1
fi

# Get registry URL from terraform output
print_info "Getting registry URL from Terraform..."
REGISTRY_URL=$(terraform output -raw registry_url 2>/dev/null)
if [ $? -ne 0 ]; then
    print_error "Failed to get registry URL. Make sure Terraform has been applied."
    exit 1
fi

print_info "Registry URL: $REGISTRY_URL"

# Configure Docker authentication
print_info "Configuring Docker authentication..."
LOCATION=$(echo $REGISTRY_URL | cut -d'-' -f1)
gcloud auth configure-docker ${LOCATION}-docker.pkg.dev --quiet

if [ $? -eq 0 ]; then
    print_info "Docker authentication configured successfully"
else
    print_error "Failed to configure Docker authentication"
    exit 1
fi

# Function to build and push image
build_and_push() {
    local IMAGE_NAME=$1
    local TAG=${2:-latest}
    
    if [ -z "$IMAGE_NAME" ]; then
        print_error "Image name is required"
        echo "Usage: $0 build <image-name> [tag]"
        exit 1
    fi
    
    FULL_IMAGE_NAME="${REGISTRY_URL}/${IMAGE_NAME}:${TAG}"
    
    print_info "Building image: $FULL_IMAGE_NAME"
    docker build -t $FULL_IMAGE_NAME .
    
    if [ $? -eq 0 ]; then
        print_info "Build successful. Pushing image..."
        docker push $FULL_IMAGE_NAME
        
        if [ $? -eq 0 ]; then
            print_info "Image pushed successfully: $FULL_IMAGE_NAME"
        else
            print_error "Failed to push image"
            exit 1
        fi
    else
        print_error "Build failed"
        exit 1
    fi
}

# Function to pull image
pull_image() {
    local IMAGE_NAME=$1
    local TAG=${2:-latest}
    
    if [ -z "$IMAGE_NAME" ]; then
        print_error "Image name is required"
        echo "Usage: $0 pull <image-name> [tag]"
        exit 1
    fi
    
    FULL_IMAGE_NAME="${REGISTRY_URL}/${IMAGE_NAME}:${TAG}"
    
    print_info "Pulling image: $FULL_IMAGE_NAME"
    docker pull $FULL_IMAGE_NAME
    
    if [ $? -eq 0 ]; then
        print_info "Image pulled successfully: $FULL_IMAGE_NAME"
    else
        print_error "Failed to pull image"
        exit 1
    fi
}

# Function to list images
list_images() {
    print_info "Listing images in registry..."
    gcloud artifacts docker images list $REGISTRY_URL
}

# Main script logic
case "${1:-help}" in
    "build")
        build_and_push $2 $3
        ;;
    "push")
        build_and_push $2 $3
        ;;
    "pull")
        pull_image $2 $3
        ;;
    "list")
        list_images
        ;;
    "auth")
        print_info "Docker authentication already configured"
        ;;
    "help"|*)
        echo "Container Registry Helper Script"
        echo ""
        echo "Usage: $0 <command> [arguments]"
        echo ""
        echo "Commands:"
        echo "  build <image-name> [tag]  - Build and push image to registry"
        echo "  pull <image-name> [tag]   - Pull image from registry"
        echo "  list                      - List all images in registry"
        echo "  auth                      - Configure Docker authentication"
        echo "  help                      - Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 build my-app latest"
        echo "  $0 pull my-app v1.0.0"
        echo "  $0 list"
        ;;
esac
