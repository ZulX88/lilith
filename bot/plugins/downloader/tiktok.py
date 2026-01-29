import requests
import urllib.parse

async def execute(client, m, text, **kwargs):
    if not text:
        return await m.reply("*Link tiktoknya?*")

    await m.react("⏳")

    try:
        res = requests.get(
            f"https://tikwm.com/api/?url={urllib.parse.quote(text)}"
        ).json()

        response = res["data"]

        if response.get("images"):
            if len(response["images"]) == 1:
                await client.send_image(m.chat, response["images"][0])
            elif len(response["images"]) > 1:
                await client.send_album(m.chat, response["images"])
            await m.react("✅")

        # Jika konten berupa video
        elif response.get("play"):
            await client.send_video(m.chat, response["play"])
            await m.react("✅")

        else:
            await m.reply("*Konten tidak ditemukan!*")
            await m.react("❌")

    except Exception as e:
        await m.reply(f"*Terjadi error:* `{e}`")
        await m.react("❌")

plugin={
    "name":"tiktok download",
    "command":"tiktok",
    "alias":["tt","tikdl"],
    "category":"Downloader",
    "exec":execute
}