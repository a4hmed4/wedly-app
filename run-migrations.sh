#!/bin/bash

# WedlyApp - Run Migrations on Cloud Run
# This script runs migrations on the deployed Cloud Run service

set -e

echo "🚀 Running migrations on Cloud Run..."

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

echo -e "${YELLOW}📋 Running migrations on: $SERVICE_NAME${NC}"

# Run migrations using Cloud Run Jobs
gcloud run jobs create migrate-job \
    --image $IMAGE_NAME \
    --region $REGION \
    --set-env-vars "DEBUG=False,SECRET_KEY=django-insecure-=om$f*08=)8i=gmqzud!ql@k=)bsknx-bct32^v^(=qn0vad@l,ALLOWED_HOSTS=wedly-app-258355634687.me-central1.run.app,localhost,127.0.0.1,PORT=8080,DJANGO_SETTINGS_MODULE=wedding_project.settings,DATABASE_URL=postgresql://postgres:Wedly%40%402025@db.kbdloigsvdrxqngrflvb.supabase.co:5432/postgres" \
    --command "python" \
    --args "manage.py,migrate,--noinput" \
    --memory 1Gi \
    --cpu 1 \
    --max-retries 3 \
    --parallelism 1 \
    --task-count 1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Migration job created successfully!${NC}"
    echo ""
    echo -e "${YELLOW}🚀 Executing migration job...${NC}"
    
    # Execute the job
    gcloud run jobs execute migrate-job --region $REGION --wait
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Migrations completed successfully!${NC}"
        echo ""
        echo -e "${YELLOW}🧹 Cleaning up migration job...${NC}"
        gcloud run jobs delete migrate-job --region $REGION --quiet
        echo -e "${GREEN}✅ Migration job cleaned up!${NC}"
    else
        echo -e "${RED}❌ Migration failed!${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Failed to create migration job!${NC}"
    exit 1
fi
