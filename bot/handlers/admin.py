from pyrogram import Client, filters
from pyrogram.types import Message
from ..player import player
from ..config import Config

def is_admin(_, __, message: Message) -> bool:
    """Check if user is admin in the chat."""
    if message.chat.type == "private":
        return True
    return message.from_user.id in Config.SUDO_USERS

# Admin filter
admin_filter = filters.create(is_admin)

# Command: /restart
@Client.on_message(filters.command("restart") & admin_filter)
async def restart_command(client: Client, message: Message):
    await message.reply("Restarting bot...")
    await client.restart()

# Command: /logs
@Client.on_message(filters.command("logs") & admin_filter)
async def logs_command(client: Client, message: Message):
    try:
        with open("bot.log", "r") as f:
            logs = f.read()
        await message.reply(f"```{logs[-4000:]}```")
    except Exception as e:
        await message.reply(f"Error getting logs: {e}")

# Command: /ping
@Client.on_message(filters.command("ping") & admin_filter)
async def ping_command(client: Client, message: Message):
    start = message.date
    reply = await message.reply("Pinging...")
    end = reply.date
    ping = (end - start).total_seconds() * 1000
    await reply.edit_text(f"Pong! {ping:.2f}ms")

# Command: /leave
@Client.on_message(filters.command("leave") & admin_filter)
async def leave_command(client: Client, message: Message):
    chat_id = message.chat.id
    if player.is_playing(chat_id):
        await player.stop(chat_id)
    await message.reply("Left voice chat!") 