# Use the official Python 3.10 image as the base image
FROM python:3.10
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg pulseaudio

COPY requirements.txt requirements.txt
# Install Python packages from requirements.txt
RUN pip install -r requirements.txt

# Copy files into the container
COPY . .

# Set environment variables
ENV DATABASE_FILE=/db/birdcage.db \
    API_SERVER_PORT=7007 \
    TEMP_DIR_NAME=tmp \
    DETECTION_DIR_NAME=detections \
    CORS_ORIGINS=* \
    REDIS_SERVER=redis \
    REDIS_PORT=6379

# Grant execution permission to start_app.sh
RUN chmod +x start_app.sh

# Start the app
CMD ["./start_app.sh"]
