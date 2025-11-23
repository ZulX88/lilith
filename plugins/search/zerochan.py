from lib.scrape import zero

async def execx(client ,m,text ,**kwargs):
    if not text:
        return await m.reply("*Nyari gambar apa?*")
    try:
        await m.react("⏳")
        searchz = zero(text,limit=10)
        await m.react("⌛")
        await client.send_album(m.chat ,searchz,quoted=m.message)
        await m.react("✅")
    except Exception as err:
        await m.react("❌")
        await m.reply(err)

plugin={
    "name":"Zerochan Search",
    "command":"zerochan",
    "alias":["zero","zerosearch","zerochansearch","zero-s","zs"],
    "exec":execx
}