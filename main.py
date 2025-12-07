# main.py
import time
import asyncio
import logging
import os
import signal
import sys
from pathlib import Path
import importlib.util

from neonize.aioze.client import NewAClient
from neonize.aioze.events import (
    CallOfferEv,
    ConnectedEv,
    MessageEv,
    PairStatusEv,
    ReceiptEv,
)
from neonize.utils import log

import config
from handler import handler  

sys.path.insert(0, os.getcwd())

# Setup logging
log.setLevel(logging.NOTSET)

# Init client
client = NewAClient(config.namedb)

class Uptime:
    start = time.time() 
    
    @classmethod
    def seconds(cls):
        return time.time() - cls.start
        
    @classmethod
    def human(cls):
        s = int(cls.seconds())
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

def load_plugins():
    plugins_dir = Path(__file__).parent / "plugins"
    if not plugins_dir.exists():
        print("❌ Folder plugins tidak ditemukan!")
        client.plugins = []
        client.command_plugins = {}
        return

    client.plugins = []          
    client.command_plugins = {}  

    for plugin_file in plugins_dir.rglob("*.py"):
        if plugin_file.name.startswith("__"):
            continue

        try:
            rel_path = plugin_file.relative_to(plugins_dir)
            module_name = f"plugin.{rel_path.with_suffix('').as_posix().replace('/', '.')}"
            spec = importlib.util.spec_from_file_location(module_name, plugin_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if not hasattr(module, "plugin") or not isinstance(module.plugin, dict):
                print(f"⚠️  Skip {rel_path}: tidak ada 'plugin' dict")
                continue

            plugin_data = module.plugin
            exec_func = plugin_data.get("exec")

            if not callable(exec_func):
                print(f"⚠️  Skip {rel_path}: 'exec' tidak valid")
                continue

            client.plugins.append({
                "exec": exec_func,
                "config": plugin_data
            })

            cmd_name = plugin_data.get("command")
            if isinstance(cmd_name, str) and cmd_name.strip():
                cmd_key = cmd_name.lower().strip()
                cmd_record = {
                    "command": cmd_name.strip(),
                    "name": plugin_data.get("name") or cmd_name.strip(),
                    "category": plugin_data.get("category", "uncategorized"),
                    "exec": exec_func,
                    "owner": bool(plugin_data.get("owner", False)),
                    "admin": bool(plugin_data.get("admin", False)),
                    "botAdmin": bool(plugin_data.get("botAdmin", False)),
                }
                client.command_plugins[cmd_key] = cmd_record
                aliases = plugin_data.get("alias", [])
                if isinstance(aliases, list):
                    for alias in aliases:
                        if isinstance(alias, str) and alias.strip():
                            alias_key = alias.lower().strip()
                            client.command_plugins[alias_key] = cmd_record
                        
                print(f"✅ Command plugin: {cmd_key}")
            else:
                print(f"✅ Logic plugin: {rel_path}")

        except Exception as e:
            print(f"❌ Gagal load {plugin_file.name}: {e}")

    print(f"⚡ {len(client.plugins)} plugin dimuat ({len(client.command_plugins)} command).")


# --- Event Handlers ---
@client.event(ConnectedEv)
async def on_connected(_: NewAClient, __: ConnectedEv):
    print("\n⚡ Connected")

@client.event(ReceiptEv)
async def on_receipt(_: NewAClient, receipt: ReceiptEv):
    log.debug(receipt)

@client.event(CallOfferEv)
async def on_call(_: NewAClient, call: CallOfferEv):
    log.debug(call)

@client.event(MessageEv)
async def on_message(client: NewAClient, message: MessageEv):
    await handler(client, message)

@client.event(PairStatusEv)
async def on_pair_status(_: NewAClient, message: PairStatusEv):
    print(f"\n✅ Logged in as {message.ID.User}")
    
# --- Main Function ---
async def connect():
    load_plugins()  
    await client.connect()
    await client.idle() 

if __name__ == "__main__":
    try:
        client.loop.run_until_complete(connect())
    except KeyboardInterrupt:
        print("\n👋 Program dihentikan.")