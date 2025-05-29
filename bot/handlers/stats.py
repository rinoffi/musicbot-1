from pyrogram import Client, filters
from pyrogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient
from ..config import Config

# Initialize MongoDB client
mongo_client = AsyncIOMotorClient(Config.MONGO_URI)
db = mongo_client.musicbot
stats = db.stats

# Command: /mystats
@Client.on_message(filters.command("mystats"))
async def mystats_command(client: Client, message: Message):
    user_id = message.from_user.id
    
    # Get user stats
    user_stats = await stats.find_one({"user_id": user_id})
    if not user_stats:
        await message.reply("You haven't played any songs yet!")
        return
        
    # Format stats
    text = f"**Your Stats:**\n\n"
    text += f"Total Songs Played: {user_stats.get('total_plays', 0)}\n"
    text += f"Total Duration: {user_stats.get('total_duration', 0)} seconds\n"
    
    # Get top tracks
    top_tracks = user_stats.get('top_tracks', [])[:5]
    if top_tracks:
        text += "\n**Top Tracks:**\n"
        for i, track in enumerate(top_tracks, 1):
            text += f"{i}. {track['title']} ({track['plays']} plays)\n"
            
    await message.reply(text)

# Command: /toptracks
@Client.on_message(filters.command("toptracks"))
async def toptracks_command(client: Client, message: Message):
    # Get top tracks across all users
    top_tracks = await stats.aggregate([
        {"$unwind": "$top_tracks"},
        {"$group": {
            "_id": "$top_tracks.title",
            "total_plays": {"$sum": "$top_tracks.plays"}
        }},
        {"$sort": {"total_plays": -1}},
        {"$limit": 10}
    ]).to_list(length=10)
    
    if not top_tracks:
        await message.reply("No tracks have been played yet!")
        return
        
    # Format response
    text = "**Top Tracks:**\n\n"
    for i, track in enumerate(top_tracks, 1):
        text += f"{i}. {track['_id']} ({track['total_plays']} plays)\n"
        
    await message.reply(text)

# Update stats when a song is played
async def update_stats(user_id: int, song_title: str, duration: int):
    # Update total plays and duration
    await stats.update_one(
        {"user_id": user_id},
        {
            "$inc": {
                "total_plays": 1,
                "total_duration": duration
            }
        },
        upsert=True
    )
    
    # Update top tracks
    await stats.update_one(
        {"user_id": user_id},
        {
            "$push": {
                "top_tracks": {
                    "$each": [{"title": song_title, "plays": 1}],
                    "$sort": {"plays": -1},
                    "$slice": 10
                }
            }
        },
        upsert=True
    ) 