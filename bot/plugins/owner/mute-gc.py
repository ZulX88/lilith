from bot.handler import update_group_ban, is_group_banned
import json

async def execx(client ,m ,text, **kwargs):
    try:
        if not text:
            return await m.reply("*Mau ngapain?*")

        user_data = m.chat.User

        if text.lower() == "on":
            if is_group_banned(user_data):
                return await m.reply("*Grup sudah dimute sebelumnya!*")
            update_group_ban(user_data, "add")
            return await m.reply("*Sukses mute grup!*")

        elif text.lower() == "off":
            if not is_group_banned(user_data):
                return await m.reply("*Grup tidak dalam mode mute!*")
            update_group_ban(user_data, "remove")
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
