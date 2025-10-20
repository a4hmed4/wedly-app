# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=wedding_project.settings
ENV PORT=8080

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create directories
RUN mkdir -p /app/media /app/static

# Run Django setup
RUN python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput --clear

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "🚀 Starting WedlyApp..."\n\
\n\
# Set environment variables\n\
export DJANGO_SETTINGS_MODULE=wedding_project.settings\n\
export PYTHONPATH=/app\n\
\n\
# Run migrations if DATABASE_URL is set\n\
if [ ! -z "$DATABASE_URL" ]; then\n\
    echo "📊 Running database migrations..."\n\
    python manage.py migrate --noinput\n\
fi\n\
\n\
# Collect static files\n\
echo "📁 Collecting static files..."\n\
python manage.py collectstatic --noinput --clear\n\
\n\
echo "✅ Django setup complete!"\n\
\n\
# Start Gunicorn with dynamic port\n\
echo "🚀 Starting Gunicorn server on port $PORT..."\n\
exec gunicorn wedding_project.wsgi:application \\\n\
    --bind 0.0.0.0:$PORT \\\n\
    --workers 1 \\\n\
    --timeout 120 \\\n\
    --keep-alive 2 \\\n\
    --max-requests 1000 \\\n\
    --max-requests-jitter 100\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:$PORT/api/accounts/profile/ || exit 1

# Start the application
CMD exec gunicorn wedding_project.wsgi:application --bind 0.0.0.0:$PORT
