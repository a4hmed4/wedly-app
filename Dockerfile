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


# Collect static files only (no database connection needed)
RUN python manage.py collectstatic --noinput --clear


# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:$PORT/api/accounts/profile/ || exit 1

# Start the application
#CMD exec gunicorn wedding_project.wsgi:application --bind 0.0.0.0:$PORT
CMD [ "bash", "-c", "python manage.py migrate && gunicorn wedding_project.wsgi:application --bind 0.0.0.0:$PORT" ]

