FROM python:3.11-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libxshmfence1 \
    libxkbcommon0 \
    libxss1 \
    libxtst6 \
    fonts-liberation \
    libappindicator3-1 \
    libnspr4 \
    libdrm2 \
    libxext6 \
    libxfixes3 \
    libxrender1 \
    libxi6 \
    libdbus-1-3 \
    libatk1.0-0 \
    libpangocairo-1.0-0 \
    libcups2 \
    libgdk-pixbuf2.0-0 \
    libpango-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Playwright and its dependencies
RUN pip install playwright
RUN playwright install --with-deps

# Copy project
COPY . .

# Expose the port
EXPOSE 8000

# Start the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
