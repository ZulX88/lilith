"""
Core Message Handler.
"""

import os
import traceback
from datetime import datetime
from termcolor import colored
from .lib.serialize import Mess
import json
from typing import List, Dict, Any, Optional
from collections import deque
import threading
from .lib.database import cache_manager
from . import config
import asyncio

from .lib.msg_store import save_message_to_store, store

_USER_BAN_CACHE = None
_GROUP_BAN_CACHE = None
_OWN_BOT_CACHE = None
_OWNER_CACHE = set(config.owner) if hasattr(config, 'owner') else set()

def _load_ban_caches():
    """
    Synchronizes local memory with database state.
    Utilizes O(1) Set lookup for ban validation performance.
    """
    global _USER_BAN_CACHE, _GROUP_BAN_CACHE, _OWN_BOT_CACHE
    
    if _USER_BAN_CACHE is None:
        _USER_BAN_CACHE = cache_manager.user_ban_cache.copy()
        _GROUP_BAN_CACHE = cache_manager.group_ban_cache.copy()
        
        JSON_DIR = "bot/database"
        filename = os.path.join(JSON_DIR, "alt_owner.json")
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    _OWN_BOT_CACHE = set(json.load(f))
            except:
                _OWN_BOT_CACHE = set()
        else:
            _OWN_BOT_CACHE = set()

def is_user_banned(user_id: str) -> bool:
    """Interface for external plugins to verify user privilege status."""
    global _USER_BAN_CACHE
    if _USER_BAN_CACHE is None:
        _load_ban_caches()
    return user_id in _USER_BAN_CACHE

def is_group_banned(group_id: str) -> bool:
    """Interface for external plugins to verify group-level restrictions."""
    global _GROUP_BAN_CACHE
    if _GROUP_BAN_CACHE is None:
        _load_ban_caches()
    return group_id in _GROUP_BAN_CACHE

async def get_group_info_cached(client, chat_jid, timeout=300):
    """
    Adaptive caching mechanism for Group Metadata.
    Reduces RPC overhead by serving valid TTL-based local state.
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
    Verifies administrative privileges with Cross-Reference (JID/LID).
    Optimized for massive groups using Set Intersection.
    """
    if not group_info:
        return False

    group_id = group_info.JID.User if hasattr(group_info, 'JID') and group_info.JID else "unknown"
    sender_id = sender.User

    cached_status = cache_manager.get_admin_status_cached(group_id, sender_id)
    if cached_status is not None:
        return cached_status

    if hasattr(group_info, 'Participants'):
        admin_jids = set()
        for p in group_info.Participants:
            jid = p.JID.User if hasattr(p, 'JID') and p.JID else None
            lid = p.LID.User if hasattr(p, 'LID') and p.LID else None
            
            if p.IsAdmin or p.IsSuperAdmin:
                if jid: admin_jids.add(jid)
                if lid: admin_jids.add(lid)
        
        is_admin = sender_id in admin_jids
    else:
        is_admin = False

    cache_manager.set_admin_status_cached(group_id, sender_id, is_admin)
    return is_admin

def is_message_duplicate(chat_id, sender_id, msg_id):
    """Prevents double-processing of events during network re-sync."""
    return cache_manager.is_duplicate_message(chat_id, sender_id, msg_id)

def update_user_ban(user_id: str, action: str = "add"):
    """Atomic update for User Ban Set and Database Persistance."""
    global _USER_BAN_CACHE
    
    if action == "add":
        cache_manager.add_user_to_ban(user_id)
        if _USER_BAN_CACHE is not None:
            _USER_BAN_CACHE.add(user_id)
    elif action == "remove":
        cache_manager.remove_user_from_ban(user_id)
        if _USER_BAN_CACHE is not None:
            _USER_BAN_CACHE.discard(user_id)

def update_group_ban(group_id: str, action: str = "add"):
    """Atomic update for Group Ban Set and Database Persistance."""
    global _GROUP_BAN_CACHE
    
    if action == "add":
        cache_manager.add_group_to_ban(group_id)
        if _GROUP_BAN_CACHE is not None:
            _GROUP_BAN_CACHE.add(group_id)
    elif action == "remove":
        cache_manager.remove_group_from_ban(group_id)
        if _GROUP_BAN_CACHE is not None:
            _GROUP_BAN_CACHE.discard(group_id)

def _extract_command_parts(budy: str, prefix_list: List[str]):
    """
    High-performance string tokenizer for command parsing.
    Bypasses heavy regex in favor of direct string indexing.
    """
    if not budy:
        return False, "", "", ""
    
    for p in prefix_list:
        if budy.startswith(p):
            content = budy[len(p):].strip()
            if not content:
                return True, p, "", ""
            
            space_idx = content.find(' ')
            if space_idx != -1:
                return True, p, content[:space_idx].lower(), content[space_idx+1:]
            return True, p, content.lower(), ""
    
    return False, "", "", ""

async def handler(client, message):
    """
    Main Execution Pipeline.
    Orchestrates validation, serialization, and plugin dispatching.
    """
    try:
        if _USER_BAN_CACHE is None:
            _load_ban_caches()
        
        m = Mess(client, message)
        
        if is_message_duplicate(m.chat.User, m.sender.User, m.id):
            return

        asyncio.create_task(save_message_to_store(client, message))

        if hasattr(client, 'my_func') and hasattr(client.my_func, 'set_expiration'):
            msg = message.Message
            msg_fields = msg.ListFields()
            if msg_fields:
                _, field_value = msg_fields[0]
                if hasattr(field_value, "contextInfo") and field_value.contextInfo:
                    ci = field_value.contextInfo
                    if hasattr(ci, 'expiration') and ci.expiration:
                        client.my_func.set_expiration(m.chat.User, ci.expiration)

        budy = m.text or ""
        is_cmd, matched_prefix, command_name, text = _extract_command_parts(budy, config.prefix)

        is_group = m.is_group
        groupMetadata = None
        
        sender_id = m.sender.User if m.sender.Server == "s.whatsapp.net" else None
        is_owner = sender_id in _OWNER_CACHE if sender_id else False
        
        if not is_owner and m.sender.Server == "lid":
            try:
                pn = await client.get_pn_from_lid(m.sender)
                is_owner = pn.User in _OWNER_CACHE
            except:
                is_owner = False
        
        if not is_owner and _OWN_BOT_CACHE:
            is_owner = (m.sender.User in _OWN_BOT_CACHE) if m.sender.Server == "s.whatsapp.net" else False
            
        if m.sender.User in _USER_BAN_CACHE:
            return
            
        if is_group and m.chat.User in _GROUP_BAN_CACHE and not is_owner:
            return
            
        if getattr(config, 'public', True) == False and not is_owner:
            return
            
        if not is_owner and not is_group:
            return

        is_admin = False
        isBotAdmin = False

        if is_group:
            groupMetadata = await get_group_info_cached(client, m.chat)
            
            if is_cmd or any(plugin.get("config", {}).get("admin") for plugin in client.plugins):
                if groupMetadata:
                    is_admin = await check_admin_status_cached(client, groupMetadata, m.sender)
                    
                    if is_cmd or any(plugin.get("config", {}).get("botAdmin") for plugin in client.plugins):
                        user_bot = await client.get_me()
                        isBotAdmin = await check_admin_status_cached(client, groupMetadata, user_bot.LID)

        # Primary Router: Command Mapping
        if is_cmd and command_name in client.command_plugins:
            cmd_info = client.command_plugins[command_name]
            
            if cmd_info.get("owner", False) and not is_owner:
                await m.reply("❌ Kamu bukan owner!")
                return
                
            if cmd_info.get("admin", False) and not (is_owner or is_admin):
                await m.reply("❌ Perlu jadi admin grup!")
                return
                
            if cmd_info.get("botAdmin", False) and not isBotAdmin:
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
                body=budy,
                store=store
            )
            
            _log_plugin(cmd_info.get("name", "unknown"), m, is_group, groupMetadata, command_name)
            return

        for plugin in client.plugins:
            config_data = plugin.get("config", {})
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
                    body=budy,
                    store=store
                )
                
                if handled:
                    mod_name = plugin["exec"].__module__.split(".")[-1]
                    _log_plugin(mod_name, m, is_group, groupMetadata, "")
                    break
                    
            except Exception as e:
                print(f"❌ Logic plugin error: {e}")
                traceback.print_exc()

    except Exception as err:
        print(f"❌ Fatal error in handler pipeline: {err}")
        traceback.print_exc()


def _log_plugin(name, m, is_group, groupMetadata, command):
    """Execution Command Log."""
    now = datetime.now().strftime('%H:%M')
    gc_name = groupMetadata.GroupName.Name if (groupMetadata and groupMetadata.GroupName) else ""
    log_msg = f'[{now}] {name}{" (" + command + ")" if command else ""} by {m.pushname or "Unknown"} : {m.sender.User}'
    
    if is_group and gc_name:
        log_msg += f' in {gc_name}'
        
    print("\n" + colored(log_msg, 'white', 'on_blue'))

_load_ban_caches()
