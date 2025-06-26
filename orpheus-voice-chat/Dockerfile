# Use Python 3.11 slim image 
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libasound2-dev \
    portaudio19-dev \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Set environment variables for the exact local app
ENV PYTHONPATH=/app:/app/src
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Create health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/ || exit 1

# Expose port for Cloud Run
EXPOSE 8080

# Use gunicorn to serve the app (same as local but production-ready)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 --preload app:app
