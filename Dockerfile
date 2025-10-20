# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=wedding_project.settings \
    PORT=8080

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends build-essential libpq-dev gettext \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create static/media directories
RUN mkdir -p /app/static /app/media

# Set permissions (optional)
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

# Expose Cloud Run port
EXPOSE 8080

# Use entrypoint script for migration + gunicorn
ENTRYPOINT ["bash", "entrypoint.sh"]
