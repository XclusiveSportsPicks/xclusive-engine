# backend/Dockerfile
FROM python:3.12-slim

# Install OS-level deps for Playwright
RUN apt-get update && apt-get install -y \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 \
    libpango-1.0-0 libpangocairo-1.0-0 libxshmfence1 libglib2.0-0 \
    libgtk-3-0 libdrm2 curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1) Copy everything in one go
COPY . .

# 2) Install Python deps
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 3) Install Playwright deps & browsers
RUN playwright install-deps && \
    playwright install

# 4) Expose and start via Gunicorn
ENV FLASK_ENV=production
EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "3"]
