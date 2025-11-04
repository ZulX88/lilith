import os
import tempfile
import yt_dlp
from youtubesearchpython import VideosSearch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def execute(client, m, text, **kwargs):
    if not text:
        return await m.reply("❌ Masukkan query pencarian YouTube!")
    
    await m.react("🔍")
    
    try:
        search = VideosSearch(text, limit=1)
        results = search.result()
        
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
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(tempfile.gettempdir(), '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'postprocessor_args': [
                '-ar', '44100',
            ],
            'prefer_ffmpeg': True,
            'audioquality': '0',
            'extractaudio': True,
            'audioformat': 'mp3',
        }
        
        # Check if cookies file exists using environment variable
        cookies_path = os.getenv('YT_COOKIES_PATH', os.path.join('lib', 'cookies.txt'))
        if os.path.exists(cookies_path):
            ydl_opts['cookiefile'] = cookies_path
        
        await m.react("⏳")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            audio_path = os.path.join(tempfile.gettempdir(), f"{info['title']}.mp3")
            
            if not os.path.exists(audio_path):
                original_filename = ydl.prepare_filename(info)
                audio_path = original_filename.rsplit('.', 1)[0] + '.mp3'
                
        info_text = f"🎵 *Judul:* {title}\n"
        info_text += f"📺 *Channel:* {channel}\n"
        if duration != 'Unknown':
            info_text += f"⏱️ *Durasi:* {duration}\n"
        if views != 'Unknown':
            info_text += f"👁️ *Views:* {views}\n"
        info_text += f"🔗 *Link:* {video_url}"
        
        await client.send_message(m.chat, info_text, link_preview=True, quoted=m)
        
        await client.send_audio(m.chat, audio_path, quoted=m.message)
        
        try:
            os.remove(audio_path)
        except:
            pass  
        
        await m.react("✅")
        
    except Exception as e:
        await m.reply(f"❌ Terjadi kesalahan: {str(e)}")
        await m.react("❌")
        try:
            if 'audio_path' in locals() and os.path.exists(audio_path):
                os.remove(audio_path)
        except:
            pass

plugin = {
    "name": "Play Audio YouTube",
    "command": "play-audio",
    "alias": ["play", "playaudio", "ytplay", "ytaudio"],
    "category": "downloader",
    "exec": execute
}