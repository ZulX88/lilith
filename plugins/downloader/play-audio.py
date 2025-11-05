from py_yt import VideosSearch
import httpx
import config

async def execute(client, m, text, **kwargs):
    if not text:
        return await m.reply("❌ Masukkan query pencarian YouTube!")
    
    await m.react("🔍")
    
    try:
        search = VideosSearch(text, limit=1)
        results = await search.next()
        
        if not results['result']:
            await m.reply("❌ Video tidak ditemukan!")
            await m.react("❌")
            return
            
        video = results['result'][0]
        video_url = video['link']
        title = video.get('title', 'Unknown')
        channel = video.get('channel', {}).get('name', 'Unknown')
        duration = video.get('duration', 'Unknown')
        views = video.get('viewCount', {}).get('short', 'Unknown')
        
        await m.react("⏳")
                
        info_text = f"🎵 *Judul:* {title}\n"
        info_text += f"📺 *Channel:* {channel}\n"
        if duration != 'Unknown':
            info_text += f"⏱️ *Durasi:* {duration}\n"
        if views != 'Unknown':
            info_text += f"👁️ *Views:* {views}\n"
        info_text += f"🔗 *Link:* {video_url}"
                
        await client.send_message(m.chat, info_text, link_preview=True,ghost_mentions=f"{m.sender.User}",mentions_are_lids=m.addressing=="LID")
        
        async with httpx.AsyncClient(headers={"X-Api-Key":config.apikeys["nauval"]}) as client:
            resp = await client.get(f"https://ytdlpyton.nvlgroup.my.id/download/audio?url={video_url}")
            response=resp.json()
        
        await client.send_audio(m.chat, response["download_url"], quoted=m.message)
        
        
        
        await m.react("✅")
        
    except Exception as e:
        await m.reply(f"❌ Terjadi kesalahan: {str(e)}")
        await m.react("❌")

plugin = {
    "name": "Play Audio YouTube",
    "command": "play-audio",
    "alias": ["play", "playaudio", "ytplay", "ytaudio"],
    "category": "downloader",
    "exec": execute
}