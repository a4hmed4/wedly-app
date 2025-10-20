# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=wedding_project.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    build-essential \
    libpq-dev \
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

# Expose port
EXPOSE 8080

# Start the application
CMD ["gunicorn", "wedding_project.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "120"]