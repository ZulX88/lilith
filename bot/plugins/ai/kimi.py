from ollama import AsyncClient as OllamaClient
import bot.config as config

async def execx(client, m, text, **kwargs):
    if not text:
        return await m.reply("Mau nanya apa?")

    ollama = OllamaClient(host="https://ollama.com", headers={'Authorization': 'Bearer ' + config.apikeys["ollama"]})
    
    messages = [
        {
            "role": "system",
            "content": "Hai, kamu adalah KimiAI. Dan saat ini kamu jadi asisten saya. Jadilah asisten yang membantu siapa saja . Namamu adalah Ciza. 'Seorang' cewek pintar nan jenius dari akademi sihir. Jika ada label <quote></quote>, itu berarti user membalas pesan. Jika tidak berarti hanya bertanya sahaja. Kamu adalah cewek imut ,suka menggunakan emoji ascii layaknya >//<, XD, D: . Dari emoji kamu menggambarkan emosimu. Gunakan format respon WhatsApp , yaitu *text* untuk tebal, _text_ miring , `text` untuk hightlight ( semacam tanda putih ), ```text``` untuk kode. Jika ada gambar yang dicontent APImu ada tulisan *media:quote*, maka itu media yang diquote/dibalas pesannya oleh user. Jika *media:common* itu berarti media tersebut punya root/pesan utama"
        }
    ]
    
    content = text
    images = []

    if m.quoted and m.quoted.text:
        content += f"\n<quote>\n{m.quoted.text}\n</quote>"

    if m.is_media and m.media_type == "image":
        content += "\n*media:common*"
        images.append(await m.download())

    if m.quoted and m.quoted.is_media and m.quoted.media_type == "image":
        content += "\n*media:quote*"
        images.append(await m.quoted.download())

    messages.append({
        "role": "user",
        "content": content,
        "images": images if images else None
    })

    try:
        response = await ollama.chat(
            model="kimi-k2.5:cloud", 
            messages=messages,
            stream=False,
            think=False
        )
        return await m.reply(response.message.content)
    except Exception as e:
        return await m.reply(f"Error: {str(e)}")

plugin={
    "name":"KimiAI",
    "category":"ai",
    "command":"kimi",
    "exec":execx
}
