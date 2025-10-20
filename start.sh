#!/bin/bash

# Startup script for Google Cloud Run
set -e

echo "🚀 Starting WedlyApp on Google Cloud Run..."

# Wait for database to be ready (if using Cloud SQL)
if [ ! -z "$CLOUD_SQL_CONNECTION_NAME" ]; then
    echo "⏳ Waiting for Cloud SQL connection..."
    sleep 10
fi

# Run migrations
echo "📊 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if needed (only in development)
if [ "$CREATE_SUPERUSER" = "true" ]; then
    echo "👤 Creating superuser..."
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
EOF
fi

# Start the application
echo "🌐 Starting Gunicorn server..."
exec gunicorn wedding_project.wsgi:application -c gunicorn.conf.py
