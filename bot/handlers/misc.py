from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp
from ..config import Config

# Command: /lyrics
@Client.on_message(filters.command("lyrics"))
async def lyrics_command(client: Client, message: Message):
    if not Config.GENIUS_API_TOKEN:
        await message.reply("Lyrics feature is not enabled!")
        return
        
    # Get song name
    query = " ".join(message.command[1:])
    if not query:
        await message.reply("Please provide a song name!")
        return
        
    # Search Genius
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.genius.com/search",
            params={"q": query},
            headers={"Authorization": f"Bearer {Config.GENIUS_API_TOKEN}"}
        ) as response:
            if response.status != 200:
                await message.reply("Error searching for lyrics!")
                return
                
            data = await response.json()
            if not data["response"]["hits"]:
                await message.reply("No lyrics found!")
                return
                
            # Get first result
            song = data["response"]["hits"][0]["result"]
            
            # Get lyrics
            async with session.get(
                f"https://api.genius.com/songs/{song['id']}",
                headers={"Authorization": f"Bearer {Config.GENIUS_API_TOKEN}"}
            ) as response:
                if response.status != 200:
                    await message.reply("Error getting lyrics!")
                    return
                    
                song_data = await response.json()
                lyrics = song_data["response"]["song"]["lyrics"]
                
                # Send lyrics
                await message.reply(f"**{song['title']}**\n\n{lyrics[:4000]}")

# Command: /help
@Client.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    text = """**Music Bot Commands:**

🎵 Music Commands:
/play <song name> - Search and play a song
/skip - Skip current song
/pause - Pause playback
/resume - Resume playback
/stop - Stop playback
/queue - Show current queue
/nowplaying - Show current song

📊 Stats Commands:
/mystats - Show your stats
/toptracks - Show top tracks

🎼 Other Commands:
/lyrics <song name> - Get song lyrics
/help - Show this help message

Admin Commands:
/restart - Restart the bot
/logs - Show bot logs
/ping - Check bot latency
/leave - Leave voice chat"""
    
    await message.reply(text) 