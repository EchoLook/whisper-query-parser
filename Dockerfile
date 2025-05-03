FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV WHISPER_MODEL=base
ENV DEFAULT_LANGUAGE=auto-detect
ENV EXPORT_DIR=/app/exports

# Create export directory
RUN mkdir -p /app/exports

# Expose the port the app runs on
EXPOSE 8000

# Command to run the API server
CMD ["python", "api_run.py"] 