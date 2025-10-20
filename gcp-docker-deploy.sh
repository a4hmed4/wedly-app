#!/bin/bash

# Google Cloud Docker Deployment Script for WedlyApp

echo "🐳 Deploying WedlyApp with Docker to Google Cloud..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK not found. Please install it first:"
    echo "https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if logged in
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "🔐 Please login to Google Cloud:"
    gcloud auth login
fi

# Set project (replace with your project ID)
PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "📋 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy using Cloud Build
echo "🚀 Building and deploying with Cloud Build..."
gcloud builds submit --config cloudbuild.yaml .

# Get the service URL
SERVICE_URL=$(gcloud run services describe wedlyapp --platform=managed --region=us-central1 --format="value(status.url)")
echo "✅ Deployment complete!"
echo "🌐 Your app is available at: $SERVICE_URL"
echo ""
echo "📝 Next steps:"
echo "1. Update environment variables in Cloud Run console"
echo "2. Configure custom domain if needed"
echo "3. Set up database (Cloud SQL or Firestore)"
echo "4. Configure email settings"
