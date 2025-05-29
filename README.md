# Railway-Optimized Advanced Telegram Music Bot

A lightweight, feature-rich Telegram music bot for group voice chats, optimized for Railway deployment.

## Features

- 🎵 YouTube search & streaming
- 📋 Queue system with limits
- 👑 Admin controls
- 📊 Usage statistics
- 🎼 Lyrics support (optional)
- 🐳 Docker & Railway ready

## Quick Start

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/musicbot.git
   cd musicbot
   ```

2. Copy `.env.example` to `.env` and fill in your values:
   ```bash
   cp .env.example .env
   ```

3. Build and run with Docker:
   ```bash
   docker build -t musicbot .
   docker run --env-file .env musicbot
   ```

4. Deploy to Railway:
   - Create a new project
   - Connect your repository
   - Add environment variables
   - Deploy!

## Configuration

Required environment variables:
- `API_ID`: Your Telegram API ID
- `API_HASH`: Your Telegram API hash
- `BOT_TOKEN`: Your bot token from @BotFather
- `MONGO_URI`: MongoDB connection string
- `SUDO_USERS`: Space-separated list of admin user IDs
- `LOG_GROUP_ID`: Group ID for logging (optional)

Optional:
- `GENIUS_API_TOKEN`: For lyrics support

## Commands

### Music Commands
- `/play <song name>` - Search and play a song
- `/skip` - Skip current song
- `/pause` - Pause playback
- `/resume` - Resume playback
- `/stop` - Stop playback
- `/queue` - Show current queue
- `/nowplaying` - Show current song

### Stats Commands
- `/mystats` - Show your stats
- `/toptracks` - Show top tracks

### Other Commands
- `/lyrics <song name>` - Get song lyrics
- `/help` - Show help message

### Admin Commands
- `/restart` - Restart the bot
- `/logs` - Show bot logs
- `/ping` - Check bot latency
- `/leave` - Leave voice chat

## Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the bot:
   ```bash
   python -m bot.main
   ```

## License

MIT License - feel free to use this project for your own bots! 