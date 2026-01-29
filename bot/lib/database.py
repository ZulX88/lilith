"""
Database helper
"""

import glob
import json
import os
import asyncio
from typing import Dict, Any, Optional
from collections import deque

JSON_DIR = "database"

all_db: Dict[str, Any] = {}

for filename in glob.glob(os.path.join(JSON_DIR, "*.json")):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        db_key = os.path.basename(filename).removesuffix(".json")
        all_db[db_key] = data
        print(f"Successfully loaded: {db_key} ✅")

    except Exception as err:
        print(f"Failed loading {filename}: {err}")

user_ban = all_db.get("user_ban", [])
group_ban = all_db.get("group_ban", [])
own_bot = all_db.get("alt_owner", [])

# =====================================================

class CacheManager:
    def __init__(self):
        # In-memory cache
        self.group_cache: Dict[str, Any] = {}
        self.user_cache: Dict[str, Any] = {}
        self.ban_cache: Dict[str, Any] = {}

        self.user_ban_cache: set[str] = set()
        self.group_ban_cache: set[str] = set()

        self.anti_duplicate = deque(maxlen=10_000)

        self.group_cache_timeout = 300
        self.admin_cache: Dict[str, tuple[bool, int]] = {}
        self.admin_cache_timeout = 300

        self._load_to_cache()

    # ---------------- internal ----------------

    def _load_to_cache(self):
        try:
            self._load_bans_to_cache()
        except Exception as e:
            print(f"Cache load error: {e}")

    def _load_bans_to_cache(self):
        self.user_ban_cache = self._load_set("bot/database/user_ban.json")
        self.group_ban_cache = self._load_set("bot/database/group_ban.json")

    @staticmethod
    def _load_set(path: str) -> set[str]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()

    # ---------------- ban checks ----------------

    def is_user_banned(self, user_id: str) -> bool:
        return user_id in self.user_ban_cache

    def is_group_banned(self, group_id: str) -> bool:
        return group_id in self.group_ban_cache

    # ---------------- modify bans ----------------

    def add_user_to_ban(self, user_id: str):
        if user_id in self.user_ban_cache:
            return

        self.user_ban_cache.add(user_id)
        self._write_list("bot/database/user_ban.json", self.user_ban_cache)

    def remove_user_from_ban(self, user_id: str):
        self.user_ban_cache.discard(user_id)
        self._write_list("bot/database/user_ban.json", self.user_ban_cache)

    def add_group_to_ban(self, group_id: str):
        if group_id in self.group_ban_cache:
            return

        self.group_ban_cache.add(group_id)
        self._write_list("bot/database/group_ban.json", self.group_ban_cache)

    def remove_group_from_ban(self, group_id: str):
        self.group_ban_cache.discard(group_id)
        self._write_list("bot/database/group_ban.json", self.group_ban_cache)

    @staticmethod
    def _write_list(path: str, data: set[str]):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sorted(data), f, indent=4)

    # ---------------- anti duplicate ----------------

    def is_duplicate_message(self, chat_id: str, sender_id: str, msg_id: str) -> bool:
        key = f"{chat_id}:{sender_id}:{msg_id}"
        if key in self.anti_duplicate:
            return True
        self.anti_duplicate.append(key)
        return False

    # ---------------- group cache ----------------

    def get_group_info_cached(
        self, group_id: str, timestamp: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        if group_id not in self.group_cache:
            return None

        data, saved_time = self.group_cache[group_id]
        now = timestamp or int(asyncio.get_running_loop().time())

        if (now - saved_time) < self.group_cache_timeout:
            return data

        return None

    def set_group_info_cached(self, group_id: str, data: Any):
        now = int(asyncio.get_running_loop().time())
        self.group_cache[group_id] = (data, now)

    # ---------------- admin cache ----------------

    def get_admin_status_cached(self, group_id: str, user_id: str) -> Optional[bool]:
        key = f"{group_id}:{user_id}"
        if key not in self.admin_cache:
            return None

        is_admin, saved_time = self.admin_cache[key]
        now = int(asyncio.get_running_loop().time())

        if (now - saved_time) < self.admin_cache_timeout:
            return is_admin

        return None

    def set_admin_status_cached(self, group_id: str, user_id: str, is_admin: bool):
        now = int(asyncio.get_running_loop().time())
        self.admin_cache[f"{group_id}:{user_id}"] = (is_admin, now)
       
cache_manager = CacheManager()