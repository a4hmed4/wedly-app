# Use Python 3.11 slim image
FROM python:3.11-slim

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=wedding_project.settings

# Working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency file and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Make static/media directories
RUN mkdir -p /app/static /app/media

# Collect static files and migrate DB
RUN python manage.py collectstatic --noinput && python manage.py migrate --noinput

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Command to start Gunicorn (Cloud Run automatically provides $PORT)
CMD exec gunicorn wedding_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120
