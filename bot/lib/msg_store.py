import asyncio
import json
import threading
import os
from dataclasses import dataclass, field
from datetime import datetime as dt
from typing import List, Dict, Optional, Any
from pathlib import Path

from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, DateTime, Boolean, Index, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func

# =========================
# SQLAlchemy Setup
# =========================

Base = declarative_base()

class MessageModel(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String, nullable=False, index=True)
    message_id = Column(String, nullable=False, unique=True, index=True)
    sender_id = Column(String, nullable=False, index=True)
    sender_id_alt = Column(String, index=True)
    content = Column(String)
    message_type = Column(String, index=True)
    timestamp = Column(DateTime, default=func.now(), index=True)
    is_group = Column(Boolean, default=False, index=True)
    quoted_message = Column(String)  # JSON string
    mentioned_jids = Column(String)  # JSON string
    raw_data = Column(LargeBinary)
    album_id = Column(String, index=True)
    
    # Index tambahan untuk performa
    __table_args__ = (
        Index('idx_chat_timestamp', 'chat_id', 'timestamp'),
        Index('idx_album_id', 'album_id'),
        Index('idx_sender_timestamp', 'sender_id', 'timestamp'),
    )

# =========================
# Proto Loader
# =========================

def load_proto(data: bytes):
    """
    Decode raw protobuf bytes → Message object
    """
    if not data:
        return None
    try:
        from neonize.proto.Neonize_pb2 import Message as BaseMessage
        msg = BaseMessage()
        msg.ParseFromString(data)
        return msg
    except Exception:
        return None


# =========================
# Data Model
# =========================

@dataclass
class StoredMessage:
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
    proto: Any = None
    
    def to_model(self) -> MessageModel:
        """Convert StoredMessage to SQLAlchemy model"""
        safe_timestamp = self.timestamp
        if safe_timestamp > 253402300799: 
            safe_timestamp = 253402300799 
        elif safe_timestamp < 0:
            safe_timestamp = 0  

        return MessageModel(
            chat_id=self.chat_id,
            message_id=self.message_id,
            sender_id=self.sender_id,
            sender_id_alt=self.sender_id_alt,
            content=self.content,
            message_type=self.message_type,
            timestamp=dt.fromtimestamp(safe_timestamp),
            is_group=self.is_group,
            quoted_message=json.dumps(self.quoted_message) if self.quoted_message else None,
            mentioned_jids=json.dumps(self.mentioned_jids) if self.mentioned_jids else None,
            raw_data=self.raw_data,
            album_id=self.album_id
        )
    
    @classmethod
    def from_model(cls, model: MessageModel) -> 'StoredMessage':
        """Convert SQLAlchemy model to StoredMessage"""
        timestamp = int(model.timestamp.timestamp())

        msg = cls(
            chat_id=model.chat_id,
            message_id=model.message_id,
            sender_id=model.sender_id,
            sender_id_alt=model.sender_id_alt,
            content=model.content,
            message_type=model.message_type,
            timestamp=timestamp,
            is_group=bool(model.is_group),
            quoted_message=json.loads(model.quoted_message) if model.quoted_message else None,
            mentioned_jids=json.loads(model.mentioned_jids) if model.mentioned_jids else [],
            raw_data=model.raw_data,
            album_id=model.album_id
        )

        # decode proto
        msg.proto = load_proto(msg.raw_data)
        return msg


# =========================
# In-Memory Store
# =========================

class InMemoryStore:
    def __init__(self):
        self._messages: Dict[str, StoredMessage] = {}  # message_id -> StoredMessage
        self._messages_by_chat: Dict[str, List[str]] = {}
        self._messages_by_album: Dict[str, List[str]] = {}
        self._messages_list: List[StoredMessage] = []  
        self._lock = threading.Lock()

    def add_message(self, stored_msg: StoredMessage):
        """Add message to in-memory store"""
        with self._lock:
            self._messages[stored_msg.message_id] = stored_msg
            self._messages_list.append(stored_msg)
            if stored_msg.chat_id not in self._messages_by_chat:
                self._messages_by_chat[stored_msg.chat_id] = []
            self._messages_by_chat[stored_msg.chat_id].append(stored_msg.message_id)
            if stored_msg.album_id:
                if stored_msg.album_id not in self._messages_by_album:
                    self._messages_by_album[stored_msg.album_id] = []
                self._messages_by_album[stored_msg.album_id].append(stored_msg.message_id)

    def get_message_by_index(self, index: int) -> Optional[StoredMessage]:
        """Get message by index from in-memory store"""
        if 0 <= index < len(self._messages_list):
            return self._messages_list[index]
        return None

    def get_message(self, message_id: str) -> Optional[StoredMessage]:
        """Get message by ID from in-memory store"""
        return self._messages.get(message_id)

    def get_messages(self, msg_ids: List[str]) -> List[StoredMessage]:
        """Get multiple messages by IDs from in-memory store"""
        return [self._messages[mid] for mid in msg_ids if mid in self._messages]

    def get_messages_by_chat_id(self, chat_id: str, limit: int = 100) -> List[StoredMessage]:
        """Get messages by chat ID from in-memory store"""
        if chat_id not in self._messages_by_chat:
            return []

        message_ids = self._messages_by_chat[chat_id][-limit:]  
        return [self._messages[mid] for mid in message_ids if mid in self._messages]

    def get_messages_by_album_id(self, chat_id: str, album_id: str, limit: int = 100) -> List[StoredMessage]:
        """Get messages by album ID from in-memory store"""
        if album_id not in self._messages_by_album:
            return []

        message_ids = [mid for mid in self._messages_by_album[album_id]
                      if self._messages[mid].chat_id == chat_id][-limit:]  
        return [self._messages[mid] for mid in message_ids if mid in self._messages]

    def get_all_messages(self) -> List[StoredMessage]:
        """Get all messages as a list for index-based access"""
        return self._messages_list.copy()

    def get_message_count(self) -> int:
        """Get total count of messages in memory"""
        return len(self._messages_list)

    def clear(self):
        """Clear all data in memory store"""
        with self._lock:
            self._messages.clear()
            self._messages_by_chat.clear()
            self._messages_by_album.clear()
            self._messages_list.clear()


# =========================
# Database Manager
# =========================

class DatabaseManager:
    def __init__(self, db_path: str = "bot/database/msg_db.sqlite3"):
        db_dir = os.path.dirname(os.path.abspath(db_path))
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        self.db_path = db_path
        self.engine = create_engine(
            f"sqlite+pysqlite:///{db_path}", 
            echo=False,
            connect_args={"check_same_thread": False}
        )
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def save_message(self, stored_msg: StoredMessage):
        """Save single message to database"""
        db = self.SessionLocal()
        try:
            model = stored_msg.to_model()
            existing = db.query(MessageModel).filter(MessageModel.message_id == stored_msg.message_id).first()
            if existing:
                for attr, value in vars(model).items():
                    if attr != 'id' and not attr.startswith('_'): 
                        setattr(existing, attr, value)
            else:
                db.add(model)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def save_messages_batch(self, stored_messages: List[StoredMessage]):
        """Save multiple messages to database in batch"""
        db = self.SessionLocal()
        try:
            for msg in stored_messages:
                model = msg.to_model()
                existing = db.query(MessageModel).filter(MessageModel.message_id == msg.message_id).first()
                if existing:
                    for attr, value in vars(model).items():
                        if attr != 'id' and not attr.startswith('_'):
                            setattr(existing, attr, value)
                else:
                    db.add(model)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def get_message_by_id(self, message_id: str) -> Optional[StoredMessage]:
        """Get message by ID from database"""
        db = self.SessionLocal()
        try:
            model = db.query(MessageModel).filter(MessageModel.message_id == message_id).first()
            if model:
                return StoredMessage.from_model(model)
            return None
        finally:
            db.close()

    def get_messages_by_user(self, chat_id: str, user_id: str, limit: int = 10) -> List[StoredMessage]:
        """Fetch messages matching chat_id and (sender_id or sender_id_alt)"""
        db = self.SessionLocal()
        try:
            models = db.query(MessageModel).filter(
                MessageModel.chat_id == chat_id,
                or_(
                    MessageModel.sender_id == user_id,
                    MessageModel.sender_id_alt == user_id
                )
            ).order_by(MessageModel.timestamp.desc()).limit(limit).all()
            return [StoredMessage.from_model(m) for m in models]
        finally:
            db.close()
    
    def get_messages_by_chat_id(self, chat_id: str, limit: int = 100) -> List[StoredMessage]:
        """Get messages by chat ID from database"""
        db = self.SessionLocal()
        try:
            models = db.query(MessageModel)\
                      .filter(MessageModel.chat_id == chat_id)\
                      .order_by(MessageModel.timestamp.desc())\
                      .limit(limit)\
                      .all()
            return [StoredMessage.from_model(model) for model in models]
        finally:
            db.close()
    
    def get_messages_by_album_id(self, chat_id: str, album_id: str, limit: int = 100) -> List[StoredMessage]:
        """Get messages by album ID from database"""
        db = self.SessionLocal()
        try:
            models = db.query(MessageModel)\
                      .filter(MessageModel.chat_id == chat_id, MessageModel.album_id == album_id)\
                      .order_by(MessageModel.timestamp.desc())\
                      .limit(limit)\
                      .all()
            return [StoredMessage.from_model(model) for model in models]
        finally:
            db.close()


# =========================
# Message Store Manager
# =========================

class MessageStore:
    def __init__(self, db_path: str = "bot/database/msg_db.sqlite3"):
        self.in_memory_store = InMemoryStore()
        self.db_manager = DatabaseManager(db_path)
        self.save_lock = threading.Lock()

    async def save_message(self, stored_msg: StoredMessage):
        """Save message to both in-memory store and database"""
        self.in_memory_store.add_message(stored_msg)
        await asyncio.get_event_loop().run_in_executor(None, self._save_to_db, stored_msg)

    def _save_to_db(self, stored_msg: StoredMessage):
        """Internal method to save message to database (runs in thread pool)"""
        with self.save_lock:
            self.db_manager.save_message(stored_msg)

    async def save_messages_batch(self, stored_messages: List[StoredMessage]):
        """Save multiple messages to both in-memory store and database"""
        for msg in stored_messages:
            self.in_memory_store.add_message(msg)
        await asyncio.get_event_loop().run_in_executor(None, self.db_manager.save_messages_batch, stored_messages)

    def get_message_by_index(self, index: int) -> Optional[StoredMessage]:
        """Get message by index from in-memory store"""
        return self.in_memory_store.get_message_by_index(index)

    def get_message(self, message_id: str) -> Optional[StoredMessage]:
        """Get message by ID (check memory first, then database)"""
        msg = self.in_memory_store.get_message(message_id)
        if msg:
            return msg
        return self.db_manager.get_message_by_id(message_id)

    def get_messages_by_user(self, chat_id: str, user_id: str, limit: int = 10) -> List[StoredMessage]:
        """Get messages by user within a chat (combine memory and database)"""
        # Manual memory filter
        mem_messages = [
            msg for msg in self.in_memory_store.get_messages_by_chat_id(chat_id, 100)
            if msg.sender_id == user_id or msg.sender_id_alt == user_id
        ]
        
        if len(mem_messages) >= limit:
            return mem_messages[:limit]
            
        needed = limit - len(mem_messages)
        db_messages = self.db_manager.get_messages_by_user(chat_id, user_id, needed)
        return mem_messages + db_messages

    def get_messages_by_chat_id(self, chat_id: str, limit: int = 100) -> List[StoredMessage]:
        """Get messages by chat ID (combine memory and database)"""
        mem_messages = self.in_memory_store.get_messages_by_chat_id(chat_id, limit)
        if len(mem_messages) >= limit:
            return mem_messages[:limit]

        needed = limit - len(mem_messages)
        db_messages = self.db_manager.get_messages_by_chat_id(chat_id, needed)
        return mem_messages + db_messages

    def get_all_messages(self) -> List[StoredMessage]:
        """Get all messages from in-memory store"""
        return self.in_memory_store.get_all_messages()

    async def save_store_to_file(self):
        """Save all messages from memory store to database file"""
        all_messages = self.in_memory_store.get_all_messages()
        if not all_messages:
            return
        await asyncio.get_event_loop().run_in_executor(None, self.db_manager.save_messages_batch, all_messages)

store = MessageStore()

# =========================
# Helper: event → StoredMessage
# =========================

async def save_message_to_store(client, message_ev):
    """
    Simpan message event ke store (memory + database)
    """
    try:
        from .serialize import Mess
        from neonize.utils import get_message_type

        m = Mess(client, message_ev)

        try:
            raw_type = get_message_type(message_ev.Message)
            message_type = str(raw_type.__name__ if hasattr(raw_type, '__name__') else type(raw_type).__name__)
        except Exception:
            message_type = "unknown"

        album_id = None
        if hasattr(message_ev, "Message"):
            proto_msg = message_ev.Message
            if proto_msg.ListFields():
                for _, field_val in proto_msg.ListFields():
                    if hasattr(field_val, "messageAssociation"):
                        assoc = field_val.messageAssociation
                        if assoc and assoc.associationType == 1:
                            album_id = assoc.parentMessageKey.ID

        raw_bytes = message_ev.SerializeToString()
        timestamp = message_ev.Info.Timestamp
        if timestamp > 2147483647:
            timestamp = timestamp // 1000  

        stored_msg = StoredMessage(
            chat_id=message_ev.Info.MessageSource.Chat.User,
            message_id=message_ev.Info.ID,
            sender_id=m.sender.User,
            sender_id_alt=m.sender_alt.User if m.sender_alt else "",
            content=m.text or "",
            message_type=message_type,
            timestamp=int(timestamp),
            is_group=message_ev.Info.MessageSource.IsGroup,
            raw_data=raw_bytes,
            album_id=album_id,
            proto=message_ev
        )

        await store.save_message(stored_msg)

    except Exception as e:
        print(f"[msg_store] save_message_to_store error: {e}")
