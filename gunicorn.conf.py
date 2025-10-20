# Gunicorn configuration for Google Cloud Run
import os

# Server socket - use PORT environment variable for Cloud Run
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"
backlog = 2048

# Worker processes
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "wedlyapp"

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# SSL (not needed for Cloud Run)
keyfile = None
certfile = None

# Environment variables
raw_env = [
    'DJANGO_SETTINGS_MODULE=wedding_project.settings',
]

# Preload app for better performance
preload_app = True

# Worker timeout
graceful_timeout = 30

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Django startup commands
def on_starting(server):
    """Run Django commands on startup"""
    import subprocess
    import sys
    
    print("🚀 Starting WedlyApp...")
    
    # Run migrations
    print("📊 Running database migrations...")
    subprocess.run([sys.executable, "manage.py", "migrate", "--noinput"], check=True)
    
    # Collect static files
    print("📁 Collecting static files...")
    subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput", "--clear"], check=True)
    
    print("✅ Django setup complete!")
