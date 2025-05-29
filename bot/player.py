from typing import Dict, Optional
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioStream
from queue import queue, Song
import asyncio
from config import Config

class Player:
    def __init__(self, calls: PyTgCalls):
        self.calls = calls
        self.active_chats: Dict[int, bool] = {}  # chat_id -> is_playing
        self.current_song: Dict[int, Song] = {}  # chat_id -> current song
        
    async def start(self):
        """Start the player and set up event handlers."""
        @self.calls.on_stream_end()
        async def on_stream_end(update: Update):
            chat_id = update.chat_id
            if chat_id in self.active_chats:
                self.active_chats[chat_id] = False
                await self.play_next(chat_id)
                
    async def play(self, chat_id: int, song: Song) -> bool:
        """Play a song in a voice chat."""
        try:
            # Get audio URL
            audio_url = await youtube.get_audio_url(song.url)
            if not audio_url:
                return False
                
            # Start playing
            await self.calls.join_group_call(
                chat_id,
                AudioStream(
                    audio_url,
                    audio_parameters={
                        'bitrate': 48000,
                    }
                )
            )
            
            self.active_chats[chat_id] = True
            self.current_song[chat_id] = song
            return True
            
        except Exception as e:
            print(f"Error playing song: {e}")
            return False
            
    async def play_next(self, chat_id: int):
        """Play the next song in queue."""
        if not queue.is_empty(chat_id):
            next_song = queue.get(chat_id)
            await self.play(chat_id, next_song)
        else:
            # Cleanup after delay
            await asyncio.sleep(Config.CLEANUP_DELAY)
            if chat_id in self.active_chats and not self.active_chats[chat_id]:
                await self.stop(chat_id)
                
    async def stop(self, chat_id: int):
        """Stop playback and cleanup."""
        try:
            await self.calls.leave_group_call(chat_id)
        except:
            pass
        finally:
            self.active_chats.pop(chat_id, None)
            self.current_song.pop(chat_id, None)
            queue.clear(chat_id)
            
    async def pause(self, chat_id: int) -> bool:
        """Pause playback."""
        try:
            await self.calls.pause_stream(chat_id)
            return True
        except:
            return False
            
    async def resume(self, chat_id: int) -> bool:
        """Resume playback."""
        try:
            await self.calls.resume_stream(chat_id)
            return True
        except:
            return False
            
    def is_playing(self, chat_id: int) -> bool:
        """Check if music is playing in chat."""
        return self.active_chats.get(chat_id, False)
        
    def get_current_song(self, chat_id: int) -> Optional[Song]:
        """Get currently playing song in chat."""
        return self.current_song.get(chat_id) 