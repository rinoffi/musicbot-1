FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install wheel
RUN python -m pip install --no-cache-dir --upgrade pip==25.1.1 && \
    pip install --no-cache-dir --upgrade setuptools wheel

# Install tgcrypto separately first
RUN pip install --no-cache-dir tgcrypto==1.2.5

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with verbose output
RUN pip install --no-cache-dir -v -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the bot
CMD ["python", "-m", "bot.main"] 