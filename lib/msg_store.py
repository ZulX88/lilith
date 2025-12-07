"""
Message store | source : github:=Nubuki-all/neon_bot
"""
import asyncio
import pickle
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime as dt
from collections import deque
import threading


@dataclass
class StoredMessage:
    """Struktur pesan yang disimpan"""
    chat_id: str
    message_id: str
    sender_id: str
    sender_id_alt: str
    content: str
    message_type: str
    timestamp: int
    is_group: bool = False
    quoted_message: Optional[Dict] = None
    mentioned_jids: List[str] = field(default_factory=list)
    raw_data: bytes = b""
    album_id: Optional[str] = None  


class MessageStore:
    def __init__(self, storage_file: str = "messages_cache.pkl"):
        self.storage_file = storage_file
        self.messages: List[StoredMessage] = []
        self._lock = threading.Lock()
        self._load_from_file()
    
    def _load_from_file(self):
        """Load messages dari file jika ada"""
        try:
            if Path(self.storage_file).exists():
                with open(self.storage_file, 'rb') as f:
                    self.messages = pickle.load(f)
        except Exception as e:
            print(f"Warning: Could not load message store: {e}")
            self.messages = []
    
    def _save_to_file(self):
        """Save messages ke file"""
        try:
            with open(self.storage_file, 'wb') as f:
                pickle.dump(self.messages, f)
        except Exception as e:
            print(f"Error saving message store: {e}")
    
    async def save_message(self, stored_msg: StoredMessage):
        """Simpan pesan ke cache dan file"""
        with self._lock:
            self.messages.append(stored_msg)
            if len(self.messages) > 10000:  
                self.messages = self.messages[-5000:]  # Keep 5000 
            self._save_to_file()
    
    async def save_messages(self, msg_list: List[StoredMessage]):
        """Simpan banyak pesan sekaligus"""
        with self._lock:
            self.messages.extend(msg_list)
            if len(self.messages) > 10000:
                self.messages = self.messages[-5000:]
            self._save_to_file()
    
    async def get_messages(self, 
                          chat_ids: List[str] = None, 
                          msg_ids: List[str] = None, 
                          limit: int = 50,
                          msg_types: List[str] = None) -> List[StoredMessage]:
        """Ambil pesan berdasarkan berbagai kriteria"""
        filtered_msgs = self.messages
        
        if chat_ids:
            chat_ids = [chat_ids] if isinstance(chat_ids, str) else chat_ids
            filtered_msgs = [msg for msg in filtered_msgs if msg.chat_id in chat_ids]
        
        if msg_ids:
            msg_ids = [msg_ids] if isinstance(msg_ids, str) else msg_ids
            filtered_msgs = [msg for msg in filtered_msgs if msg.message_id in msg_ids]
        
        if msg_types:
            msg_types = [msg_types] if isinstance(msg_types, str) else msg_types
            filtered_msgs = [msg for msg in filtered_msgs if msg.message_type in msg_types]
        
        filtered_msgs.sort(key=lambda x: x.timestamp, reverse=True)
        
        return filtered_msgs[:limit] if limit else filtered_msgs
    
    async def get_messages_by_type(self, chat_id: str, msg_type: str, limit: int = 50) -> List[StoredMessage]:
        """Ambil pesan berdasarkan chat dan tipe pesan"""
        return await self.get_messages(
            chat_ids=[chat_id], 
            msg_types=[msg_type], 
            limit=limit
        )
    
    async def get_messages_by_user(self, chat_id: str, user_id: str, limit: int = 50) -> List[StoredMessage]:
        """Ambil pesan dari user tertentu dalam chat"""
        filtered_msgs = [msg for msg in self.messages 
                        if msg.chat_id == chat_id and msg.sender_id == user_id]
        filtered_msgs.sort(key=lambda x: x.timestamp, reverse=True)
        return filtered_msgs[:limit]
    
    async def get_messages_by_album_id(self, chat_id: str, album_id: str, limit: int = 100) -> List[StoredMessage]:
        """Ambil pesan-pesan yang merupakan bagian dari album yang sama"""
        filtered_msgs = [msg for msg in self.messages 
                        if msg.chat_id == chat_id and msg.album_id == album_id]
        filtered_msgs.sort(key=lambda x: x.timestamp, reverse=True)
        return filtered_msgs[:limit]
    
    async def delete_message(self, chat_id: str, msg_id: str) -> bool:
        """Hapus pesan tertentu"""
        with self._lock:
            initial_len = len(self.messages)
            self.messages = [msg for msg in self.messages 
                           if not (msg.chat_id == chat_id and msg.message_id == msg_id)]
            deleted = initial_len != len(self.messages)
            if deleted:
                self._save_to_file()
            return deleted
    
    async def clear_chat_messages(self, chat_id: str):
        """Hapus semua pesan dari chat tertentu"""
        with self._lock:
            self.messages = [msg for msg in self.messages if msg.chat_id != chat_id]
            self._save_to_file()
    
    async def cleanup_old_messages(self, days: int = 7):
        """Bersihkan pesan lama lebih dari X hari"""
        current_time = int(dt.now().timestamp())
        cutoff_time = current_time - (days * 24 * 60 * 60)
        
        with self._lock:
            self.messages = [msg for msg in self.messages if msg.timestamp > cutoff_time]
            self._save_to_file()

message_store = MessageStore()


async def save_message_to_store(client, message_ev):
    """Fungsi helper untuk menyimpan pesan dari message event"""
    try:
        from lib.serialize import Mess
        m = Mess(client, message_ev)
        
        message_type : str = ""
        raw_data = None
        album_id = None
           
        try:
            from neonize.utils import get_message_type
            message_type = get_message_type(message_ev.Message)
        except:
            message_type = 'unknown'

        try:
            if hasattr(message_ev, 'Message'):
                raw_data = message_ev

                msg_obj = message_ev.Message
                if msg_obj.ListFields():
                    for field_desc, field_val in msg_obj.ListFields():
                        if hasattr(field_val, "messageAssociation"):
                            if hasattr(field_val.messageAssociation, "parentMessageKey") and field_val.messageAssociation.associationType == 1:
                                album_id = field_val.messageAssociation.parentMessageKey.ID

        except:
            raw_data = None
        
        stored_msg = StoredMessage(
            chat_id=message_ev.Info.MessageSource.Chat.User,
            message_id=message_ev.Info.ID,
            sender_id=m.sender.User,
            sender_id_alt=m.sender_alt.User,
            content=m.text or "",
            message_type=message_type,
            timestamp=message_ev.Info.Timestamp,
            is_group=message_ev.Info.MessageSource.IsGroup,
            raw_data=raw_data,
            album_id=album_id
        )
        
        await message_store.save_message(stored_msg)
    except Exception as e:
        print(f"Error saving message to store: {e}")

async def get_messages(chat_ids=None, msg_ids=None, limit=50, msg_types=None):
    return await message_store.get_messages(chat_ids, msg_ids, limit, msg_types)

async def get_messages_by_type(chat_id, msg_type, limit=50):
    return await message_store.get_messages_by_type(chat_id, msg_type, limit)

async def get_messages_by_user(chat_id, user_id, limit=50):
    return await message_store.get_messages_by_user(chat_id, user_id, limit)

async def get_messages_by_album_id(chat_id, album_id, limit=100):
    return await message_store.get_messages_by_album_id(chat_id, album_id, limit)