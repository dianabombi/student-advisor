"""
WEBSOCKET CONNECTION MANAGER
Manages WebSocket connections for real-time updates
"""

from typing import Dict
from fastapi import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        # Store active connections: {user_id: websocket}
        self.active_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Connect a new WebSocket client"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"User {user_id} connected via WebSocket")
    
    def disconnect(self, user_id: int):
        """Disconnect a WebSocket client"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"User {user_id} disconnected from WebSocket")
    
    async def send_personal_message(self, message: dict, user_id: int):
        """Send message to specific user"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(json.dumps(message))
            except Exception as e:
                print(f"Error sending message to user {user_id}: {e}")
                self.disconnect(user_id)
    
    async def broadcast(self, message: dict, user_ids: list = None):
        """Broadcast message to multiple users"""
        targets = user_ids if user_ids else list(self.active_connections.keys())
        
        for user_id in targets:
            await self.send_personal_message(message, user_id)
    
    def is_connected(self, user_id: int) -> bool:
        """Check if user is connected"""
        return user_id in self.active_connections
    
    def get_connected_users(self) -> list:
        """Get list of all connected user IDs"""
        return list(self.active_connections.keys())

# Global instance
ws_manager = ConnectionManager()
