import yt_dlp
from youtubesearchpython import VideosSearch
from typing import List, Dict, Optional
import asyncio
from config import Config

class YouTube:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
    async def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search YouTube and return top results."""
        try:
            videos_search = VideosSearch(query, limit=limit)
            results = videos_search.result()['result']
            
            return [{
                'title': video['title'],
                'duration': video['duration'],
                'url': f"https://youtube.com/watch?v={video['id']}",
                'thumbnail': video['thumbnails'][0]['url'],
            } for video in results]
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            return []
            
    async def get_audio_url(self, url: str) -> Optional[str]:
        """Get direct audio URL from YouTube video."""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info['url']
        except Exception as e:
            print(f"Error getting audio URL: {e}")
            return None
            
    def get_duration(self, url: str) -> Optional[int]:
        """Get video duration in seconds."""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info['duration']
        except Exception as e:
            print(f"Error getting duration: {e}")
            return None

# Global YouTube instance
youtube = YouTube() 