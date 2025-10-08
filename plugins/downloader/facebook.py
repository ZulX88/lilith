from lib.scrape import fesnuk

async def execute(client,m,text,**kwargs):
    if not text:
        return await m.reply("Kirim link facebooknya!")
    linku = fesnuk(text)
    await client.send_video(m.chat,linku,quoted=m.message)

plugin = {
    "name":"Facebook download",
    "command":"facebook",
    "alias":["fb","fesnuk","fbdl"],
    "category":"downloader",
    "exec":execute
}
