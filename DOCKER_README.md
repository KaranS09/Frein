# Docker Setup for Events Scraper + PostgreSQL

## Overview
This Docker setup runs:
1. **bookMyShow.py** - Scrapes BookMyShow events
2. **db_dump.py** - Inserts scraped data into PostgreSQL
3. **PostgreSQL** - Database to store events
4. **Cron** - Schedules daily runs at 2 AM UTC

## Files Created

- **Dockerfile** - Builds the scraper application with all dependencies
- **docker-compose.yml** - Orchestrates PostgreSQL + scraper services
- **entrypoint.sh** - Entry point that sets up cron scheduling
- **init.sql** - Database schema initialization
- **requirements.txt** - Python dependencies

## Quick Start (Local Testing)

### Prerequisites
- Docker installed
- Docker Compose installed

### Run Locally

```bash
# Navigate to project root
cd e:\Hustle\Fren\Frien

# Start containers
docker-compose up -d

# View logs
docker-compose logs -f scraper

# Stop containers
docker-compose down
```

This will:
1. Start PostgreSQL
2. Build and start the scraper container
3. Run bookMyShow.py immediately (first run)
4. Run db_dump.py to sync data
5. Schedule daily runs at 2 AM UTC via cron

### Check Database

```bash
# Access PostgreSQL directly
docker exec -it events_postgres psql -U postgres -d events_db

# View events table
SELECT * FROM events LIMIT 10;
```

## Deployment to Cloud (Fly.io Example)

### 1. Install Fly CLI
```bash
# Windows PowerShell
iwr https://fly.io/install.ps1 -useb | iex
```

### 2. Deploy
```bash
# Login to Fly
fly auth login

# Create new app
fly launch

# Deploy
fly deploy
```

### 3. Change Cron Schedule
Edit `entrypoint.sh` line:
```bash
CRON_SCHEDULE="0 2 * * *"  # Change "2" to desired hour (UTC)
```

## Environment Variables

Configure in `docker-compose.yml` or cloud deployment:
- `DB_HOST` - PostgreSQL host (default: localhost)
- `DB_PORT` - PostgreSQL port (default: 5432)
- `DB_NAME` - Database name (default: events_db)
- `DB_USER` - Database user (default: postgres)
- `DB_PASSWORD` - Database password

## Important Notes

⚠️ **Security in Production:**
- Change the hardcoded password "140703" in db_dump.py and docker-compose.yml
- Use `.env` file with secrets management
- Never commit credentials to Git

### To use .env file:
1. Create `.env` in project root:
```
DB_PASSWORD=your_secure_password
```

2. Update docker-compose.yml to reference it:
```yaml
environment:
  DB_PASSWORD: ${DB_PASSWORD}
```

## Cron Schedule Reference

```
CRON_SCHEDULE="0 2 * * *"
               │ │ │ │ │
               │ │ │ │ └─── Day of week (0-7, 0/7 = Sunday)
               │ │ │ └───── Month (1-12)
               │ │ └─────── Day of month (1-31)
               │ └───────── Hour (0-23)
               └─────────── Minute (0-59)

Current: 0 2 * * * = Every day at 2:00 AM UTC
```

## Troubleshooting

### Container won't start
```bash
docker-compose logs scraper
```

### Chrome/Chromium won't run
The Dockerfile uses chromium-browser instead of full Chrome (smaller image size). If you need full Chrome:
- Update Dockerfile to use `google-chrome-stable` instead
- Increase image size (~2GB instead of ~500MB)

### PostgreSQL connection timeout
- Check if postgres container is healthy: `docker-compose ps`
- Wait a few seconds for postgres to initialize
- Check logs: `docker-compose logs postgres`

## Volume Mounts

- `./LLM:/app/LLM` - CSV data persists locally
- `postgres_data` - Database data persists even if container stops

To preserve events across deployments, data is saved to volumes.

## Next Steps

1. Test locally first
2. Once working, push to GitHub
3. Deploy to Fly.io or your preferred cloud
4. Monitor logs regularly
5. Set up alerts if cron fails

