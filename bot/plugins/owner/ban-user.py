from bot.handler import update_user_ban, is_user_banned
import json

async def execx(client, m, text, command, **kwargs):
    try:
        target = (m.mentioned_jid[0] if m.mentioned_jid else None) or \
                 (m.quoted.sender if m.quoted else None)

        if not target:
            return await m.reply("*Tag/reply user yang mau dibanned!*")

        text_parts = text.split() if text else []
        action = text_parts[0].lower() if text_parts else ""

        pn = await client.get_pn_from_lid(target) if target.Server == "lid" else target

        match action:
            case "ban":
                if is_user_banned(pn.User):
                    return await m.reply("*User sudah di-banned sebelumnya!*")
                update_user_ban(pn.User, "add")
                await m.reply(f"*Sukses ban user*")
            case "unban":
                if not is_user_banned(pn.User):
                    return await m.reply("*User tidak ada dalam daftar ban!*")
                update_user_ban(pn.User, "remove")
                await m.reply(f"*Sukses unban user*")
            case _:
                return await m.reply("*Opsi invalid! Hanya boleh `ban`/`unban`*")

    except Exception as e:
        await m.reply(f"❌ Error: {str(e)}")

plugin = {
    "name": "User management",
    "command": "user",
    "category":"owner",
    "owner": True,
    "exec": execx
}
