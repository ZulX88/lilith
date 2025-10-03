async def execute(client, m, **kwargs):
    # Cek apakah pesan utama atau quoted punya media
    if not m.is_media and not (m.quoted and m.quoted.is_media):
        return await m.reply("*Kirim atau reply foto yang ingin dijadikan stiker*")
    
    # Tolak kalau media berupa video
    if m.media_type == "video" or (m.quoted and m.quoted.media_type == "video"):
        return await m.reply("*Video tidak bisa dijadikan stiker*")
    
    # Download media (prioritas pesan utama, fallback ke quoted)
    buffer = (
        await m.download() if m.is_media
        else await m.quoted.download() if m.quoted and m.quoted.is_media
        else None
    )

    if not buffer:
        return await m.reply("*Gagal mengunduh media*")

    # Kirim sebagai stiker
    await client.send_sticker(m.chat, buffer)


plugin = {
    "category":"misc",
    "name": "sticker",
    "command": "sticker",
    "alias": ["s", "stiker", "stc"],
    "exec": execute
}
