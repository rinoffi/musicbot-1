import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Telegram API Credentials
    API_ID = int(os.getenv("28015531"))
    API_HASH = os.getenv("2ab4ba37fd5d9ebf1353328fc915ad28")
    BOT_TOKEN = os.getenv("7965807385:AAFZiAyeZ4-tbWcw_bgDGwO-gx2Dr1A4x74")

    # MongoDB Configuration
    MONGO_URI = os.getenv("mongodb+srv://haribotx:haribotx@cluster0.i3skil4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

    # Bot Configuration
    SUDO_USERS = [int(x) for x in os.getenv("7874828505", "").split()]
    LOG_GROUP_ID = int(os.getenv("-1002365504358"))

    # Optional: Genius API for lyrics
    GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")

    # Bot Settings
    MAX_QUEUE_SIZE = 50
    MAX_DURATION = 3600  # 1 hour in seconds
    CLEANUP_DELAY = 300  # 5 minutes in seconds 
