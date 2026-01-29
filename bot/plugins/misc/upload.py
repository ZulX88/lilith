import httpx
import time
import asyncio
import secrets
import hashlib

def format_size(bytes_val):
    if not bytes_val: return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024

def generate_random_name(ext):
    # Layer 1: Random Hex
    raw_seed = secrets.token_hex(16)
    # Layer 2: Time salt
    salt = str(time.time())
    # Layer 3: SHA256 Hash
    secure_hash = hashlib.sha256(f"{raw_seed}{salt}".encode()).hexdigest()
    # Layer 4: Final Shuffle (Shorten to 12 chars for readability)
    return f"{secure_hash[:12]}{ext}"

async def execute(client, m, body, text, **kwargs):
    target = m.quoted if (m.quoted and m.quoted.is_media) else (m if m.is_media else None)
    if not target:
        return await m.reply("Reply media!")

    info = target.media_info
    raw_size = int(info.get("fileLength", 0))
    m_type = target.media_type
    mime = info.get("mimetype", "application/octet-stream").split(';')[0]
    readable_size = format_size(raw_size)
    
    ext_map = {
        "image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp",
        "video/mp4": ".mp4", "audio/mpeg": ".mp3", "audio/ogg": ".ogg"
    }
    ext = ext_map.get(mime, ".bin")
    fname = generate_random_name(ext)

    async with httpx.AsyncClient(timeout=120.0, follow_redirects=True) as session:
        buff = await target.download()
        res_url = None

        if m_type == "image" and raw_size < 5 * 1024 * 1024:
            try:
                res = await session.post("https://telegra.ph/upload?source=bugtracker", files={'file': ('file', buff)})
                res_url = f"https://telegra.ph{res.json()['src']}"
            except:
                pass

        if not res_url:
            endpoints = [
                "https://cloudkuimages.guru/",
                "https://cdn.nekohime.site/upload"
            ]
            
            for up in endpoints:
                try:
                    res = await session.post(up, files={'file': (fname, buff, mime)})
                    if res.status_code == 200:
                        data = res.json()
                        if "data" in data:
                            res_url = data['data']['url']
                        elif "files" in data:
                            res_url = data['files'][0]['url']
                        
                        if res_url: break
                except:
                    continue

        if res_url:
            await m.reply(f"*Size:* {readable_size}\n*Filename:* {fname}\n*URL:* {res_url}")
        else:
            await m.reply("Upload failed.")

plugin = {
    "name": "Uploader",
    "command": "up",
    "alias": ["upload", "tourl", "url"],
    "exec": execute
}
