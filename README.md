# Qundylyq Deployment Guide (Docker + ngrok)

This project is configured for production deployment with:
- Django + Gunicorn
- PostgreSQL
- ngrok tunnel (public HTTPS URL without router setup)

## 1. Prerequisites
- Docker and Docker Compose installed
- ngrok account and auth token

## 2. Configure Environment
Create `.env` from template:

```bash
cp .env.example .env
```

Set at least:
- `NGROK_AUTHTOKEN`
- `ALLOWED_HOSTS` (include `.ngrok-free.app`)
- `CSRF_TRUSTED_ORIGINS` (include `https://*.ngrok-free.app`)
- `DJANGO_SECRET_KEY`

Optional:
- `NGROK_DOMAIN` (only if you have a reserved/custom ngrok domain)

## 3. Start Services
From the project root:

```bash
docker compose up -d --build
```

Hot reload is enabled for the Django app: when Python/templates change, the server reloads automatically.

## 4. Verify
Check containers:

```bash
docker compose ps
```

Check logs:

```bash
docker compose logs -f ngrok web
```

Open:
- ngrok URL from logs (example: `https://abc123.ngrok-free.app`)

## 5. Optional: Create Django Admin User
```bash
docker compose exec web python backend/manage.py createsuperuser
```
