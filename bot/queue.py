from typing import Dict, List, Optional
from dataclasses import dataclass
from config import Config

@dataclass
class Song:
    title: str
    duration: int
    url: str
    thumbnail: str
    requested_by: int

class Queue:
    def __init__(self):
        self.queues: Dict[int, List[Song]] = {}  # chat_id -> list of songs
        
    def add(self, chat_id: int, song: Song) -> bool:
        """Add a song to the queue. Returns False if queue is full."""
        if chat_id not in self.queues:
            self.queues[chat_id] = []
            
        if len(self.queues[chat_id]) >= Config.MAX_QUEUE_SIZE:
            return False
            
        self.queues[chat_id].append(song)
        return True
        
    def get(self, chat_id: int) -> Optional[Song]:
        """Get the next song from the queue."""
        if not self.queues.get(chat_id):
            return None
            
        return self.queues[chat_id].pop(0) if self.queues[chat_id] else None
        
    def clear(self, chat_id: int) -> None:
        """Clear the queue for a specific chat."""
        self.queues[chat_id] = []
        
    def get_queue(self, chat_id: int) -> List[Song]:
        """Get the entire queue for a chat."""
        return self.queues.get(chat_id, [])
        
    def is_empty(self, chat_id: int) -> bool:
        """Check if queue is empty for a chat."""
        return not bool(self.queues.get(chat_id))
        
    def remove(self, chat_id: int, index: int) -> Optional[Song]:
        """Remove a song at specific index from queue."""
        if not self.queues.get(chat_id) or index >= len(self.queues[chat_id]):
            return None
            
        return self.queues[chat_id].pop(index)

# Global queue instance
queue = Queue() 