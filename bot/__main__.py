import time
import asyncio
import logging
import os
import sys
from pathlib import Path
import importlib.util
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .lib.msg_store import store
from . import config
from .handler import handler
from .lib.func import MyFunc

from neonize.aioze.client import NewAClient
from neonize.aioze.events import (
    CallOfferEv,
    ConnectedEv,
    MessageEv,
    PairStatusEv,
    ReceiptEv,
)
from neonize.utils import log

log.setLevel(logging.NOTSET)
client = NewAClient(config.namedb)

class GlobalWatcher(FileSystemEventHandler):
    def __init__(self, reload_plugins_func, restart_logic_func):
        self.reload_plugins_func = reload_plugins_func
        self.restart_logic_func = restart_logic_func
        self.last_reload = 0

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            now = time.time()
            if now - self.last_reload > 1:
                # Jika yang berubah di folder plugins, cukup reload plugins (Hot Reload)
                if "plugins" in event.src_path:
                    print(f"\n🔄 Plugin Change: {event.src_path}. Reloading plugins...")
                    self.reload_plugins_func()
                # Jika file inti (handler, config, lib), restart proses bot (Full Reload)
                else:
                    print(f"\n⚠️ Core Change: {event.src_path}. Restarting bot...")
                    os.execv(sys.executable, ['python'] + sys.argv)
                self.last_reload = now

def load_plugins():
    plugins_dir = Path(__file__).parent / "plugins"
    if not plugins_dir.exists():
        client.plugins, client.command_plugins = [], {}
        return

    client.plugins, client.command_plugins = [], {}

    for plugin_file in plugins_dir.rglob("*.py"):
        if plugin_file.name.startswith("__"): continue
        try:
            rel_path = plugin_file.relative_to(plugins_dir)
            module_name = f"bot.plugins.{rel_path.with_suffix('').as_posix().replace('/', '.')}"
            if module_name in sys.modules: del sys.modules[module_name]

            spec = importlib.util.spec_from_file_location(module_name, plugin_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "plugin") and isinstance(module.plugin, dict):
                plugin_data = module.plugin
                exec_func = plugin_data.get("exec")
                if callable(exec_func):
                    client.plugins.append({"exec": exec_func, "config": plugin_data})
                    cmd_name = plugin_data.get("command")
                    if isinstance(cmd_name, str) and cmd_name.strip():
                        cmd_key = cmd_name.lower().strip()
                        cmd_record = {
                            "command": cmd_name.strip(),
                            "name": plugin_data.get("name") or cmd_name.strip(),
                            "category": plugin_data.get("category", "misc"),
                            "exec": exec_func,
                            "owner": bool(plugin_data.get("owner", False)),
                            "admin": bool(plugin_data.get("admin", False)),
                            "botAdmin": bool(plugin_data.get("botAdmin", False)),
                        }
                        client.command_plugins[cmd_key] = cmd_record
                        for alias in plugin_data.get("alias", []):
                            if isinstance(alias, str) and alias.strip():
                                client.command_plugins[alias.lower().strip()] = cmd_record
        except Exception as e:
            print(f"❌ Error {plugin_file.name}: {e}")
    print(f"⚡ {len(client.plugins)} plugins | {len(client.command_plugins)} commands.")

async def save_store_periodically(interval_minutes=5):
    while True:
        try:
            await store.save_store_to_file()
            print(f"[{time.strftime('%H:%M:%S')}] Store auto-saved.")
        except Exception as e:
            print(f"Error save store: {e}")
        await asyncio.sleep(interval_minutes * 60)

@client.event(ConnectedEv)
async def on_connected(_: NewAClient, __: ConnectedEv):
    print("\n⚡ Connected")

@client.event(MessageEv)
async def on_message(client: NewAClient, message: MessageEv):
    await handler(client, message)

@client.event(PairStatusEv)
async def on_pair_status(_: NewAClient, message: PairStatusEv):
    print(f"\n✅ Logged in: {message.ID.User}")

async def start_bot():
    load_plugins()
    
    # Monitor seluruh folder 'bot'
    observer = Observer()
    handler_watch = GlobalWatcher(reload_plugins_func=load_plugins, restart_logic_func=None)
    observer.schedule(handler_watch, path=str(Path(__file__).parent), recursive=True)
    observer.start()

    client.my_func = MyFunc(client)
    asyncio.create_task(save_store_periodically(5))

    try:
        await client.connect()
        await client.idle()
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    try:
        client.loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        print("\n👋 Shutdown")
