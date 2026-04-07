#!/bin/bash

# entrypoint.sh - Orchestrates scraping and DB insertion with cron scheduling

set -e

echo "Starting application..."

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Create the cron job
# Schedule: Run at 2 AM every day
CRON_SCHEDULE="0 2 * * *"
CRON_JOB="$CRON_SCHEDULE cd /app && python Scraper/bookMyShow.py && python Persistence/db_dump.py >> /var/log/cron.log 2>&1"

# Write cron job to crontab
echo "$CRON_JOB" | crontab -

# Start cron daemon
echo "Starting cron scheduler..."
cron -f &

# Optional: Run scraper and db_dump immediately on startup (comment out if you don't want this)
echo "Running initial scrape and DB sync..."
python Scraper/bookMyShow.py
python Persistence/db_dump.py

echo "Application setup complete. Cron is running."
echo "Scheduled to run daily at 2 AM UTC"
echo "Logs will be written to /var/log/cron.log"

# Keep container running
wait
