FROM python:3.11-slim

# Install Chrome and dependencies for Selenium
RUN apt-get update && apt-get install -y \
    chromium-browser \
    chromium-chromedriver \
    cron \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Make scripts executable
RUN chmod +x /app/entrypoint.sh

# Set environment variables for Chrome
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV CHROME_BIN=/usr/bin/chromium-browser

# Run entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
