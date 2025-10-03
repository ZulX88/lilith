# handler.py

import traceback
from datetime import datetime
from termcolor import colored
from lib.serialize import Mess
import config

async def handler(client, message):
    try:
        async def check_owner(sender):
            if sender.Server == "s.whatsapp.net":
                return sender.User in config.owner
            elif sender.Server == "lid":
                pn = await client.get_pn_from_lid(sender)
                return pn.User in config.owner
            return False

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
        is_admin = False
        isBotAdmin = False

        if not is_owner and not is_group:
            return

        if is_group:
            try:
                groupMetadata = await client.get_group_info(m.chat)
                user_bot = await client.get_me()
                for p in groupMetadata.Participants:
                    if (p.JID.User == m.sender.User or p.LID.User == m.sender.User) and (p.IsAdmin or p.IsSuperAdmin):
                        is_admin = True
                    if p.LID.User == user_bot.LID.User and (p.IsAdmin or p.IsSuperAdmin):
                        isBotAdmin = True
                    if is_admin and isBotAdmin:
                        break
            except:
                pass

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