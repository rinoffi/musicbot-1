FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt update && apt install -y ffmpeg git && \
    pip install --no-cache-dir -U yt-dlp tgcrypto

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the bot
CMD ["python", "-m", "bot.main"] 