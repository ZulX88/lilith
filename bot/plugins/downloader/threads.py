from bot.lib.scrape import threads

async def execute(client, m, text, **kwargs):
  
    if not text:
        return await m.reply("*Link Threadsnya?*")
    
    await m.react("⏳")
    
    try:
        res = threads(text)
        
        video = res.get('video_urls', [])
        photo = res.get('image_urls', [])
        
        if not video and not photo:
            await m.reply("*Tidak ada media yang ditemukan!*")
            await m.react("❌")
            return
        
        if len(video) == 1 and len(photo) == 0:
            await client.send_video(m.chat, video[0], quoted=m.message)
        
        elif len(photo) == 1 and len(video) == 0:
            await client.send_photo(m.chat, photo[0], quoted=m.message)
        
        elif len(video) >= 1 and len(photo) >= 1:
            all_media = [*video, *photo]
            await client.send_album(m.chat, all_media, quoted=m.message)
        
        elif len(video) > 1 and len(photo) == 0:
            await client.send_album(m.chat, video, quoted=m.message)
        
        elif len(photo) > 1 and len(video) == 0:
            await client.send_album(m.chat, photo, quoted=m.message)
        
        await m.react("✅")
        
    except Exception as e:
        await m.reply(f"*Terjadi error:* `{str(e)}`")
        await m.react("❌")

plugin = {
    "name": "Threads downloader",
    "command": "threads",
    "alias": ["thdl", "threadsdl"],
    "category": "Downloader",
    "exec": execute
}