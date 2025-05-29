from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from ..youtube import youtube
from ..queue import queue, Song
from ..player import player
from ..config import Config
import asyncio

# Command: /play
@Client.on_message(filters.command("play"))
async def play_command(client: Client, message: Message):
    # Check if user is in voice chat
    if not message.from_user.voice:
        await message.reply("You need to be in a voice chat to use this command!")
        return
        
    # Get query
    query = " ".join(message.command[1:])
    if not query:
        await message.reply("Please provide a song name to play!")
        return
        
    # Search YouTube
    results = await youtube.search(query)
    if not results:
        await message.reply("No results found!")
        return
        
    # Create inline keyboard with results
    keyboard = []
    for i, result in enumerate(results):
        keyboard.append([
            InlineKeyboardButton(
                f"{i+1}. {result['title']} ({result['duration']})",
                callback_data=f"play_{result['url']}"
            )
        ])
        
    await message.reply(
        "Choose a song to play:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Callback: Play selected song
@Client.on_callback_query(filters.regex("^play_"))
async def play_callback(client: Client, callback_query):
    url = callback_query.data.split("_")[1]
    chat_id = callback_query.message.chat.id
    
    # Create song object
    song = Song(
        title=callback_query.message.reply_markup.inline_keyboard[0][0].text.split(". ")[1].split(" (")[0],
        duration=int(callback_query.message.reply_markup.inline_keyboard[0][0].text.split("(")[1].split(")")[0]),
        url=url,
        thumbnail="",  # TODO: Add thumbnail
        requested_by=callback_query.from_user.id
    )
    
    # Add to queue
    if not queue.add(chat_id, song):
        await callback_query.answer("Queue is full!")
        return
        
    # Start playing if not already playing
    if not player.is_playing(chat_id):
        await player.play(chat_id, song)
        await callback_query.answer("Started playing!")
    else:
        await callback_query.answer("Added to queue!")

# Command: /skip
@Client.on_message(filters.command("skip"))
async def skip_command(client: Client, message: Message):
    chat_id = message.chat.id
    if not player.is_playing(chat_id):
        await message.reply("Nothing is playing!")
        return
        
    await player.stop(chat_id)
    await message.reply("Skipped current song!")

# Command: /pause
@Client.on_message(filters.command("pause"))
async def pause_command(client: Client, message: Message):
    chat_id = message.chat.id
    if not player.is_playing(chat_id):
        await message.reply("Nothing is playing!")
        return
        
    if await player.pause(chat_id):
        await message.reply("Paused!")
    else:
        await message.reply("Failed to pause!")

# Command: /resume
@Client.on_message(filters.command("resume"))
async def resume_command(client: Client, message: Message):
    chat_id = message.chat.id
    if not player.is_playing(chat_id):
        await message.reply("Nothing is playing!")
        return
        
    if await player.resume(chat_id):
        await message.reply("Resumed!")
    else:
        await message.reply("Failed to resume!")

# Command: /stop
@Client.on_message(filters.command("stop"))
async def stop_command(client: Client, message: Message):
    chat_id = message.chat.id
    if not player.is_playing(chat_id):
        await message.reply("Nothing is playing!")
        return
        
    await player.stop(chat_id)
    await message.reply("Stopped playback!")

# Command: /queue
@Client.on_message(filters.command("queue"))
async def queue_command(client: Client, message: Message):
    chat_id = message.chat.id
    queue_list = queue.get_queue(chat_id)
    
    if not queue_list:
        await message.reply("Queue is empty!")
        return
        
    text = "**Current Queue:**\n\n"
    for i, song in enumerate(queue_list, 1):
        text += f"{i}. {song.title} ({song.duration}s)\n"
        
    await message.reply(text)

# Command: /nowplaying
@Client.on_message(filters.command("nowplaying"))
async def nowplaying_command(client: Client, message: Message):
    chat_id = message.chat.id
    current_song = player.get_current_song(chat_id)
    
    if not current_song:
        await message.reply("Nothing is playing!")
        return
        
    text = f"**Now Playing:**\n\n"
    text += f"Title: {current_song.title}\n"
    text += f"Duration: {current_song.duration}s\n"
    text += f"Requested by: {current_song.requested_by}"
    
    await message.reply(text) 