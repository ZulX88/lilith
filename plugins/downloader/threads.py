from lib.scrape import threads

async def execute(client, m, text, **kwargs):
    """
    Download media content from Threads.
    
    This plugin allows users to download images and videos from Threads posts
    by providing a Threads URL. It can handle both single and multiple media items.
    
    Args:
        client: The client instance
        m: The message object
        text: The Threads URL to download from
        **kwargs: Additional keyword arguments
    """
    if not text:
        return await m.reply("*Link Threadsnya?*")
    
    await m.react("⏳")
    
    try:
        res = threads(text)
        
        # Check if there are any downloadable media
        image_urls = res.get('image_urls', [])
        video_urls = res.get('video_urls', [])
        
        if not image_urls and not video_urls:
            await m.reply("*Tidak ada media yang ditemukan!*")
            await m.react("❌")
            return
        
        # Handle images
        if image_urls:
            if len(image_urls) == 1:
                await client.send_image(m.chat, image_urls[0], quoted=m.message)
            elif len(image_urls) > 1:
                await client.send_album(m.chat, image_urls, quoted=m.message)
        
        # Handle videos
        if video_urls:
            for video_url in video_urls:
                await client.send_video(m.chat, video_url, quoted=m.message)
        
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