from lib.database import group_ban
import json

async def execx(client ,m ,text, **kwargs):
    try:
        if not text:
            return await m.reply("*Mau ngapain?*")

        user_data = m.chat.User

        if text.lower() == "on":
            if user_data not in group_ban:
                group_ban.append(user_data)

            with open(f"database/group_ban.json","w") as file:
                json.dump(group_ban, file, indent=4)

            return await m.reply("*Sukses mute grup!*")

        elif text.lower() == "off":
            if user_data in group_ban:
                group_ban.remove(user_data)

            with open(f"database/group_ban.json","w") as file:
                json.dump(group_ban, file, indent=4)

            return await m.reply("*Sukses unmute grup!*")

        else:
            return await m.reply("*Opsi invalid*!!")
    except Exception as e:
        await m.reply(f"❌ Error: {str(e)}")

plugin={
    "name":"Mute group",
    "command":"mute",
    "category":"owner",
    "exec":execx,
    "owner":True
}
