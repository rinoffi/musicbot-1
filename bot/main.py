import logging
from pyrogram import Client
from pytgcalls import PyTgCalls
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Pyrogram client
app = Client(
    "musicbot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Initialize PyTgCalls
calls = PyTgCalls(app)

# Import handlers
from handlers import music, admin, stats, misc

async def main():
    # Start the client
    await app.start()
    logger.info("Bot started!")
    
    # Start PyTgCalls
    await calls.start()
    logger.info("PyTgCalls started!")
    
    # Keep the bot running
    await app.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 