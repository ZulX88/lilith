from lib.database import user_ban
import json

async def execx(client, m, text, command, **kwargs):
    target = (m.mentioned_jid[0] if m.mentioned_jid else None) or \
             (m.quoted.sender if m.quoted else None)

    if not target:
        return await m.reply("*Tag/reply user yang mau dibanned!*")

    # Parse text untuk mendapatkan aksi (ban/unban)
    text_parts = text.split() if text else []
    action = text_parts[0].lower() if text_parts else ""

    pn = await client.get_pn_from_lid(target) if target.Server == "lid" else target

    changed = False

    match action:
        case "ban":
            if pn.User not in user_ban:
                user_ban.append(pn.User)
                changed = True
            else:
                return await m.reply("*User sudah di-banned sebelumnya!*")
        case "unban":
            if pn.User in user_ban:
                user_ban.remove(pn.User)
                changed = True
            else:
                return await m.reply("*User tidak ada dalam daftar ban!*")
        case _:
            return await m.reply("*Opsi invalid! Hanya boleh `ban`/`unban`*")

    if changed:
        try:
            with open("database/user_ban.json", "w") as file:
                json.dump(user_ban, file, indent=4)
            await m.reply(f"*Sukses {action} user*")
        except Exception as e:
            await m.reply(f"*Gagal menyimpan database: {e}*")

plugin = {
    "name": "User management",
    "command": "user",
    "owner": True,
    "exec": execx
}
