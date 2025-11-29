from lib.scrape import instagram

async def execute(client ,m,text,**kwargs):
    try:
        if not text:
            return await m.reply("*Link ignya?*")
        await m.react("⏳")
        res = instagram(text)
        match res["type"]:
            case "gallery":
                await client.send_album(m.chat,res["urls"],quoted=m.message)
            case "image":
                await client.send_image(m.chat ,res["url"],quoted=m.message)
            case "video":
                await client.send_video(m.chat,res["url"],quoted=m.message)

        await m.react("✅")
    except Exception as e:
        await m.reply(f"❌ Error: {str(e)}")

plugin={
    "name":"Instagram downloader",
    "command":"instagram",
    "alias":["ig","igdl"],
    "category":"Downloader",
    "exec":execute
}