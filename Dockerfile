# ============================
# Stage: Python base
# ============================
FROM python:3.11-slim

# Environment vars
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=wedding_project.settings \
    PORT=8080

WORKDIR /app

# Install deps
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

#RUN python manage.py collectstatic --noinput && python manage.py migrate --noinput

EXPOSE 8080

# ✅ Gunicorn command — Cloud Run will inject $PORT automatically
CMD ["gunicorn", "wedding_project.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120"]
