import os
import traceback
from datetime import datetime
from termcolor import colored
from lib.serialize import Mess
import json
from typing import List, Dict, Any, Optional
from collections import deque
import threading
from lib.database import group_ban, user_ban, own_bot
import config
import asyncio
from lib.msg_store import save_message_to_store, message_store, get_messages_by_album_id


class CacheManager:
    def __init__(self):
        self.group_cache: Dict[str, Any] = {}
        self.user_cache: Dict[str, Any] = {}
        self.ban_cache: Dict[str, Any] = {}
        self.user_ban_cache: set = set()
        self.group_ban_cache: set = set()
        self.anti_duplicate = deque(maxlen=10000)
        self.group_cache_timeout = 300  # 5 menit
        self.admin_cache: Dict[str, Any] = {}
        self.admin_cache_timeout = 300  # 5 menit
        
        self._load_to_cache()

    def _load_to_cache(self):
        """Load data dari file JSON ke dalam cache memory"""
        try:
            self._load_bans_to_cache()
        except Exception as e:
            print(f"Error loading cache: {e}")

    def _load_bans_to_cache(self):
        """Load bans ke dalam set cache untuk akses lebih cepat"""
        try:
            with open("database/user_ban.json", "r") as f:
                user_ban_data = json.load(f)
            self.user_ban_cache = set(user_ban_data)
        except Exception:
            self.user_ban_cache = set()

        try:
            with open("database/group_ban.json", "r") as f:
                group_ban_data = json.load(f)
            self.group_ban_cache = set(group_ban_data)
        except Exception:
            self.group_ban_cache = set()

    def is_user_banned(self, user_id: str) -> bool:
        """Cek apakah user banned - lebih cepat karena pakai set()"""
        return user_id in self.user_ban_cache

    def is_group_banned(self, group_id: str) -> bool:
        """Cek apakah group banned - lebih cepat karena pakai set()"""
        return group_id in self.group_ban_cache

    def add_user_to_ban(self, user_id: str):
        """Tambah user ke ban cache dan file"""
        self.user_ban_cache.add(user_id)
        # Update file juga
        with open("database/user_ban.json", "r") as f:
            user_ban_list = json.load(f)
        if user_id not in user_ban_list:
            user_ban_list.append(user_id)
            with open("database/user_ban.json", "w") as f:
                json.dump(user_ban_list, f, indent=4)

    def remove_user_from_ban(self, user_id: str):
        """Hapus user dari ban cache dan file"""
        self.user_ban_cache.discard(user_id)
        # Update file juga
        with open("database/user_ban.json", "r") as f:
            user_ban_list = json.load(f)
        if user_id in user_ban_list:
            user_ban_list.remove(user_id)
            with open("database/user_ban.json", "w") as f:
                json.dump(user_ban_list, f, indent=4)

    def add_group_to_ban(self, group_id: str):
        """Tambah group ke ban cache dan file"""
        self.group_ban_cache.add(group_id)
        # Update file juga
        with open("database/group_ban.json", "r") as f:
            group_ban_list = json.load(f)
        if group_id not in group_ban_list:
            group_ban_list.append(group_id)
            with open("database/group_ban.json", "w") as f:
                json.dump(group_ban_list, f, indent=4)

    def remove_group_from_ban(self, group_id: str):
        """Hapus group dari ban cache dan file"""
        self.group_ban_cache.discard(group_id)
        # Update file juga
        with open("database/group_ban.json", "r") as f:
            group_ban_list = json.load(f)
        if group_id in group_ban_list:
            group_ban_list.remove(group_id)
            with open("database/group_ban.json", "w") as f:
                json.dump(group_ban_list, f, indent=4)

    def is_duplicate_message(self, chat_id: str, sender_id: str, msg_id: str) -> bool:
        """Cek apakah pesan duplikat menggunakan deque - sistem seperti @neon_bot/**"""
        msg_key = f"{chat_id}:{sender_id}:{msg_id}"
        if msg_key in self.anti_duplicate:
            return True
        self.anti_duplicate.append(msg_key)
        return False

    def get_group_info_cached(self, group_id: str, timestamp: int = None) -> Optional[Dict]:
        """Get group info from cache with timeout"""
        if group_id in self.group_cache:
            data, saved_time = self.group_cache[group_id]
            if timestamp is None or (timestamp - saved_time) < self.group_cache_timeout:
                return data
        return None

    def set_group_info_cached(self, group_id: str, data: Any):
        """Set group info ke cache"""
        self.group_cache[group_id] = (data, int(asyncio.get_event_loop().time()))

    def get_admin_status_cached(self, group_id: str, user_id: str) -> Optional[bool]:
        """Get admin status from cache with timeout"""
        cache_key = f"{group_id}:{user_id}"
        if cache_key in self.admin_cache:
            is_admin, saved_time = self.admin_cache[cache_key]
            current_time = int(asyncio.get_event_loop().time())
            if (current_time - saved_time) < self.admin_cache_timeout:
                return is_admin
        return None

    def set_admin_status_cached(self, group_id: str, user_id: str, is_admin: bool):
        """Set admin status to cache"""
        cache_key = f"{group_id}:{user_id}"
        self.admin_cache[cache_key] = (is_admin, int(asyncio.get_event_loop().time()))

cache_manager = CacheManager()

async def get_group_info_cached(client, chat_jid, timeout=300):
    """
    Get group info from cache first, then from API if not in cache
    """
    group_id = chat_jid.User
    cached_info = cache_manager.get_group_info_cached(group_id)
    
    if cached_info:
        return cached_info
    
    try:
        fresh_info = await client.get_group_info(chat_jid)
        cache_manager.set_group_info_cached(group_id, fresh_info)
        return fresh_info
    except Exception as e:
        print(f"Error fetching group info: {e}")
        return None


async def check_admin_status_cached(client, group_info, sender, timeout=300):
    """
    Check admin status with caching
    """
    if not group_info:
        return False

    if hasattr(group_info, 'JID') and group_info.JID:
        group_id = group_info.JID.User
    else:
        group_id = "unknown"
    
    sender_id = sender.User

    cached_status = cache_manager.get_admin_status_cached(group_id, sender_id)
    if cached_status is not None:
        return cached_status

    is_admin = False
    for p in group_info.Participants:
        if (p.JID.User == sender_id or p.LID.User == sender_id) and (p.IsAdmin or p.IsSuperAdmin):
            is_admin = True
            break

    cache_manager.set_admin_status_cached(group_id, sender_id, is_admin)
    return is_admin


def is_message_duplicate(chat_id, sender_id, msg_id):
    """
    Check if message is duplicate using anti-duplicate cache
    """
    return cache_manager.is_duplicate_message(chat_id, sender_id, msg_id)


def update_user_ban(user_id: str, action: str = "add"):
    """
    Update user ban cache and file
    """
    if action == "add":
        cache_manager.add_user_to_ban(user_id)
    elif action == "remove":
        cache_manager.remove_user_from_ban(user_id)


def update_group_ban(group_id: str, action: str = "add"):
    """
    Update group ban cache and file
    """
    if action == "add":
        cache_manager.add_group_to_ban(group_id)
    elif action == "remove":
        cache_manager.remove_group_from_ban(group_id)


async def handler(client, message):
    try:
        if is_message_duplicate(
            message.Info.MessageSource.Chat.User,
            message.Info.MessageSource.Sender.User,
            message.Info.ID
        ):
            return

        asyncio.create_task(save_message_to_store(client, message))

        async def check_owner(sender):
            if sender.Server == "s.whatsapp.net":
                uid = sender.User
            elif sender.Server == "lid":
                pn = await client.get_pn_from_lid(sender)
                uid = pn.User
            else:
                return False

            return uid in config.owner or uid in own_bot

        m = Mess(client, message)
        budy = m.text

        prefix = config.prefix
        is_cmd = False
        command_name = ""
        text = ""
        matched_prefix = ""

        for p in prefix:
            if budy.startswith(p):
                is_cmd = True
                matched_prefix = p
                content = budy[len(p):].strip()
                if content:
                    parts = content.split(" ", 1)
                    command_name = parts[0].lower()
                    text = parts[1] if len(parts) > 1 else ""
                break

        is_group = m.is_group
        groupMetadata = None
        is_owner = await check_owner(m.sender)
        
        if is_user_banned(m.sender.User) or is_user_banned(m.sender_alt.User):
            return
        if is_group and is_group_banned(m.chat.User) and not is_owner:
            return
            
        if config.public == False and not is_owner:
            return
        if not is_owner and not is_group:
            return

        is_admin = False
        isBotAdmin = False

        if is_group:
            groupMetadata = await get_group_info_cached(client, m.chat)

            if groupMetadata:
                is_admin = await check_admin_status_cached(client, groupMetadata, m.sender)

                user_bot = await client.get_me()
                isBotAdmin = await check_admin_status_cached(client, groupMetadata, user_bot.LID)

        if is_cmd and command_name in client.command_plugins:
            cmd_info = client.command_plugins[command_name]

            if cmd_info["owner"] and not is_owner:
                await m.reply("❌ Kamu bukan owner!")
                return
            if cmd_info["admin"] and not (is_owner or is_admin):
                await m.reply("❌ Perlu jadi admin grup!")
                return
            if cmd_info["botAdmin"] and not isBotAdmin:
                await m.reply("❌ Bot harus jadi admin dulu!")
                return

            await cmd_info["exec"](
                client=client,
                m=m,
                text=text,
                is_owner=is_owner,
                is_admin=is_admin,
                is_bot_admin=isBotAdmin,
                is_group=is_group,
                groupMetadata=groupMetadata,
                prefix=matched_prefix,
                command=command_name,
                body=budy
            )
            _log_plugin(cmd_info["name"], m, is_group, groupMetadata, command_name)
            return

        for plugin in client.plugins:
            config_data = plugin["config"]
            if "command" in config_data:
                continue

            try:
                handled = await plugin["exec"](
                    client=client,
                    m=m,
                    text=budy,
                    is_owner=is_owner,
                    is_admin=is_admin,
                    is_bot_admin=isBotAdmin,
                    is_group=is_group,
                    group_metadata=groupMetadata,
                    body=budy
                )
                if handled:
                    mod_name = plugin["exec"].__module__.split(".")[-1]
                    _log_plugin(mod_name, m, is_group, groupMetadata, "")
                    break
            except Exception as e:
                print(f"❌ Logic plugin error: {e}")
                traceback.print_exc()

    except Exception as err:
        print(f"❌ Fatal error: {err}")
        traceback.print_exc()


def _log_plugin(name, m, is_group, groupMetadata, command):
    now = datetime.now().strftime('%H:%M')
    gc_name = groupMetadata.GroupName.Name if (groupMetadata and groupMetadata.GroupName) else ""
    log_msg = f'[{now}] {name}{" (" + command + ")" if command else ""} by {m.pushname or "Unknown"} : {m.sender.User}'
    if is_group:
        log_msg += f' in {gc_name}'
    print("\n" + colored(log_msg, 'white', 'on_blue'))

import glob
JSON_DIR = "database"
all_db = {}
for filename in glob.glob(os.path.join(JSON_DIR, "*.json")):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        db_key = os.path.basename(filename).split(".json")[0]
        all_db[db_key] = data
    except Exception as err:
        print(err)

def is_user_banned(user_id):
    """Gunakan caching untuk performa lebih tinggi"""
    return user_id in cache_manager.user_ban_cache

def is_group_banned(group_id):
    """Gunakan caching untuk performa lebih tinggi"""
    return group_id in cache_manager.group_ban_cache

user_ban = list(cache_manager.user_ban_cache)
group_ban = list(cache_manager.group_ban_cache)
own_bot = all_db.get("alt_owner", [])