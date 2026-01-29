import asyncio

async def execute(client,m,store,**kwargs):
  if not m.quoted:
    return await m.reply("Reply image on album to stickerize! ( Minimum image 2 )")
  album_id = await m.quoted.album_id()
  mess = store.get_messages_by_album_id(chat_id=m.chat.User, album_id=album_id)
  media = [client.download_any(msgs.proto.Message) for msgs in mess]
  files = await asyncio.gather(*media)
  await client.send_stickerpack(m.chat, files, quoted=m.message, packname="You",publisher=m.pushname)

plugin ={
  "name":"stickerize album",
  "command":"stickerize",
  "exec":execute
}