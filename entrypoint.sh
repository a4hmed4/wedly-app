#!/bin/bash
set -e

echo "🚀 Starting WedlyApp..."

# Set environment variables
export DJANGO_SETTINGS_MODULE=wedding_project.settings
export PYTHONPATH=/app

# Run migrations
echo "📊 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "✅ Django setup complete!"

# Start Gunicorn
echo "🚀 Starting Gunicorn server..."
exec gunicorn wedding_project.wsgi:application -c gunicorn.conf.py
