# backend/Dockerfile
FROM python:3.12-slim

# 1) Install OS-level deps required by Playwright
RUN apt-get update && apt-get install -y \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 \
    libpango-1.0-0 libpangocairo-1.0-0 libxshmfence1 libglib2.0-0 \
    libgtk-3-0 libdrm2 curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2) Copy & install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 3) Install Playwright system deps and browsers
RUN playwright install-deps && \
    playwright install

# 4) Copy the rest of your app
COPY . .

# 5) Expose port and run via Gunicorn
ENV FLASK_ENV=production
EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "3"]
