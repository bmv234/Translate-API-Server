#!/bin/bash

# Exit on any error
set -e

echo "Starting Docker build for Translation API Server..."

# Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "Error: Docker daemon is not running"
    exit 1
fi

# Build the Docker image
echo "Building Docker image 'translation-server'..."
docker build -t translation-server . || {
    echo "Error: Docker build failed"
    exit 1
}

echo "Docker build completed successfully!"
echo "You can now run the server using:"
echo "docker run -d -p 8000:8000 translation-server:latest"