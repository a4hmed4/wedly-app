# WedlyApp Docker Setup

## Quick Start

### Development
```bash
# Build and run with SQLite
docker build -t wedlyapp .
docker run -p 8000:8000 wedlyapp

# Or use docker-compose
docker-compose up --build
```

### Production
```bash
# Copy and edit environment file
cp env.docker .env

# Run production setup
docker-compose -f docker-compose.prod.yml up --build -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

## Environment Variables

Edit `.env` file with your settings:

```bash
# Required
SECRET_KEY=your-super-secret-key
ALLOWED_HOSTS=your-domain.com,localhost

# Database (for production)
DATABASE_URL=postgresql://user:pass@db:5432/wedlyapp

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Firebase (optional)
FIRESTORE_ENABLED=true
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CREDENTIALS_JSON=path/to/service-account.json
```

## Services

- **web**: Django application (port 8000)
- **db**: PostgreSQL database (port 5432)
- **redis**: Redis cache (port 6379)
- **nginx**: Reverse proxy (port 80/443)

## Commands

```bash
# View logs
docker-compose logs -f web

# Run Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Access database
docker-compose exec db psql -U wedlyapp -d wedlyapp

# Restart services
docker-compose restart web
```

## Production Deployment

1. Set up environment variables
2. Configure domain in `ALLOWED_HOSTS`
3. Set up SSL certificates
4. Use `docker-compose.prod.yml`
5. Configure nginx for your domain

## Troubleshooting

- Check logs: `docker-compose logs web`
- Rebuild: `docker-compose up --build --force-recreate`
- Reset database: `docker-compose down -v && docker-compose up`
