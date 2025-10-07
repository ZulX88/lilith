async def execute(client, m, text, groupMetadata, **kwargs):
    target = ""
    for p in groupMetadata.Participants:
        target += f"@{p.LID.User} "

    texttag = m.quoted.text if m.quoted else text
    if not texttag:
        await m.reply("Reply atau kirim teks!")
        return

    await client.send_message(m.chat, texttag, ghost_mentions=target, mentions_are_lids=True)

plugin = {
    "name": "Hidetag",
    "command": "hidetag",
    "admin": True,
    "alias": ["ht"],
    "category": "group",
    "exec": execute
}
