from lib.scrape import YTDL
from py_yt import Search

async def execx(client ,m ,text ,command,**kwargs):
    try:
        match command:
            case "play"|"play-a":
                if not text:
                    return await m.reply("*Mau nyari apa?")
                yts=Search(text,limit=1)
                results=await yts.next()
                if not results["result"]:
                    await m.reply("❌ Video tidak ditemukan!")
                    await m.react("❌")
                    return
                result=results["result"][0]
                url = result["link"]
                title = result.get("title", "Unknown")
                channel = result.get("channel", {}).get("name", "Unknown")
                duration = result.get("duration", "Unknown")
                views = result.get("viewCount", {}).get("short", "Unknown")
                thumbnail = result.get("thumbnails",{})[0].get("url").split("&rs")[0]
                await m.react("⏳")
                info_text = f"🎵 *Judul:* {title}\n"
                info_text += f"📺 *Channel:* {channel}\n"
                if duration != "Unknown":
                    info_text += f"⏱️ *Durasi:* {duration}\n"
                if views != "Unknown":
                    info_text += f"👁️ *Views:* {views}\n"
                info_text += f"🔗 *Link:* {url}"

                await client.send_image(m.chat ,thumbnail,caption=info_text,quoted=m.message)

                yt = YTDL()
                audio_url = await yt.download(url,"128k")
                audio_url = audio_url.get("downloadUrl")
                await client.send_audio(m.chat ,audio_url,quoted=m.message)
    except Exception as e:
        await m.reply(f"❌ Error: {str(e)}")

plugin={
    "name":"Youtube downloader",
    "command":"play-a",
    "exec":execx,
    "category": "downloader"
}
        