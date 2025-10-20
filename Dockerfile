FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONHASHSEED=random \
    DJANGO_SETTINGS_MODULE=wedding_project.settings

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create and set work directory
WORKDIR /app

# Install Python dependencies (optimized)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create media and static directories
RUN mkdir -p /app/media /app/static

# Optimize Python bytecode
RUN python -m compileall . && \
    find . -name "*.py" -exec python -m py_compile {} \;

# Collect static files (optimized)
RUN python manage.py collectstatic --noinput --clear

RUN python manage.py migrate --noinput

# Make startup script executable
RUN chmod +x start.sh

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8080

# Health check - use PORT environment variable
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import os, requests; port=os.environ.get('PORT', '8080'); requests.get(f'http://localhost:{port}/api/accounts/profile/', timeout=10)" || exit 1

# Run the application
CMD ["./start.sh"]
