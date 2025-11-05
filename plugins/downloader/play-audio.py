from py_yt import VideosSearch
import httpx
import config
import os

async def execute(client, m, text, **kwargs):
    if not text:
        return await m.reply("❌ Masukkan query pencarian YouTube!")

    await m.react("🔍")

    try:
        search = VideosSearch(text, limit=1)
        results = await search.next()

        if not results["result"]:
            await m.reply("❌ Video tidak ditemukan!")
            await m.react("❌")
            return

        video = results["result"][0]
        video_url = video["link"]
        thumbnail_url = video["thumbnails"][-1]["url"]
        title = video.get("title", "Unknown")
        channel = video.get("channel", {}).get("name", "Unknown")
        duration = video.get("duration", "Unknown")
        views = video.get("viewCount", {}).get("short", "Unknown")

        await m.react("⏳")

        info_text = f"🎵 *Judul:* {title}\n"
        info_text += f"📺 *Channel:* {channel}\n"
        if duration != "Unknown":
            info_text += f"⏱️ *Durasi:* {duration}\n"
        if views != "Unknown":
            info_text += f"👁️ *Views:* {views}\n"
        info_text += f"🔗 *Link:* {video_url}"

        # --- Download thumbnail ---
        thumb_path = "/tmp/thumb.jpg"
        async with httpx.AsyncClient() as session:
            thumb_resp = await session.get(thumbnail_url)
            thumb_resp.raise_for_status()
            with open(thumb_path, "wb") as f:
                f.write(thumb_resp.content)

        # Kirim thumbnail + caption
        await client.send_image(m.chat, thumb_path, caption=info_text)

        # --- Ambil link audio dari API ---
        async with httpx.AsyncClient(headers={"X-Api-Key": config.apikeys["nauval"]}) as session:
            resp = await session.get(
                "https://ytdlpyton.nvlgroup.my.id/download/audio",
                params={"url": video_url, "mode": "url", "bitrate": "128k"},
                follow_redirects=True
            )
            resp.raise_for_status()
            response = resp.json()

        await client.send_audio(m.chat, response["download_url"], quoted=m.message)
        await m.react("✅")

        # Hapus file thumbnail biar bersih
        try:
            os.remove(thumb_path)
        except:
            pass

    except Exception as e:
        await m.reply(f"❌ Terjadi kesalahan: {str(e)}")
        await m.react("❌")


plugin = {
    "name": "Play Audio YouTube",
    "command": "play-audio",
    "alias": ["play", "playaudio", "ytplay", "ytaudio"],
    "category": "downloader",
    "exec": execute,
}