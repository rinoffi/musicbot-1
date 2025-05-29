FROM python:3.11-bullseye

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    git \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install wheel
RUN python -m pip install --no-cache-dir --upgrade pip==25.1.1 && \
    pip install --no-cache-dir --upgrade setuptools wheel

# Install packages one by one
RUN pip install --no-cache-dir pyrogram==2.0.106 && \
    pip install --no-cache-dir tgcrypto==1.2.5 && \
    pip install --no-cache-dir pytgcalls==4.0.0b3 && \
    pip install --no-cache-dir yt-dlp==2023.12.30 && \
    pip install --no-cache-dir aiohttp==3.9.1 && \
    pip install --no-cache-dir motor==3.3.2 && \
    pip install --no-cache-dir python-dotenv==1.0.0 && \
    pip install --no-cache-dir youtube-search-python==1.6.6 && \
    pip install --no-cache-dir pymongo==4.6.1 && \
    pip install --no-cache-dir cryptg==0.4.0

# Copy the application
COPY . .

# Run the bot
CMD ["python", "-m", "bot.main"] 
