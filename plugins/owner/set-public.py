import config

async def execute(client,m,text,prefix,command,**kwargs):
  try:
    if not text:
      return await m.reply(f"""Help : *{prefix}{command}* public/self""")
    cmd = text.lower()
    config.public = False if cmd == "self" else True if cmd == "public" else None
    await m.reply(f"*Sukses {cmd} bot!*")
  except Exception as e:
    await m.reply(f"❌ Error: {str(e)}")

plugin={
  "name": "Set permission of bot",
  "command": "set",
  "owner":True,
  "category":"owner",
  "exec":execute
}