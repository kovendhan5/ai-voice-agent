# Multi-stage Dockerfile for Orpheus Voice Chat - Cloud Run Optimized
FROM python:3.11-slim as builder

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    python3-pyaudio \
    espeak \
    espeak-data \
    libespeak1 \
    libespeak-dev \
    festival \
    festvox-kallpc16k \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    espeak \
    espeak-data \
    libespeak1 \
    festival \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY src/app_live_orpheus.py app_live_orpheus.py

# Create necessary directories
RUN mkdir -p /tmp/audio

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PORT=5000

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run the application
CMD ["python", "app_live_orpheus.py"]
