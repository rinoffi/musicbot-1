import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Telegram API Credentials
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI")

    # Bot Configuration
    SUDO_USERS = [int(x) for x in os.getenv("SUDO_USERS", "").split()]
    LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID"))

    # Optional: Genius API for lyrics
    GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")

    # Bot Settings
    MAX_QUEUE_SIZE = 50
    MAX_DURATION = 3600  # 1 hour in seconds
    CLEANUP_DELAY = 300  # 5 minutes in seconds 