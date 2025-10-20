#!/bin/bash

# WedlyApp - Docker Deployment Script
# This script builds and deploys the application to Google Cloud Run

set -e

echo "🚀 Starting WedlyApp Deployment..."

# Configuration
PROJECT_ID="wedly-app-475621"
SERVICE_NAME="wedly-app"
REGION="me-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📋 Deployment Configuration:${NC}"
echo "Project ID: $PROJECT_ID"
echo "Service Name: $SERVICE_NAME"
echo "Region: $REGION"
echo "Image: $IMAGE_NAME"
echo ""

# Step 1: Build Docker image
echo -e "${YELLOW}🔨 Building Docker image...${NC}"
docker build -t $IMAGE_NAME .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Docker image built successfully!${NC}"
else
    echo -e "${RED}❌ Docker build failed!${NC}"
    exit 1
fi

# Step 2: Push to Google Container Registry
echo -e "${YELLOW}📤 Pushing image to Google Container Registry...${NC}"
docker push $IMAGE_NAME

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Image pushed successfully!${NC}"
else
    echo -e "${RED}❌ Image push failed!${NC}"
    exit 1
fi

# Step 3: Deploy to Cloud Run
echo -e "${YELLOW}🚀 Deploying to Google Cloud Run...${NC}"
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --timeout 300 \
    --concurrency 100 \
    --set-env-vars "DEBUG=False,SECRET_KEY=your-secret-key-here,ALLOWED_HOSTS=wedly-app-258355634687.me-central1.run.app,PORT=8080,DJANGO_SETTINGS_MODULE=wedding_project.settings"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    echo ""
    echo -e "${GREEN}🎉 WedlyApp is now running on Google Cloud Run!${NC}"
    echo -e "${YELLOW}📝 The app is using SQLite database by default. To use Supabase, set DATABASE_URL environment variable.${NC}"
else
    echo -e "${RED}❌ Deployment failed!${NC}"
    exit 1
fi
