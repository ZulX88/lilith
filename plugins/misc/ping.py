async def execute(client, m, **kwargs):
    await m.reply("🏓 Pong!")

plugin = {
    "command": "ping",
    "name": "Ping Bot",
    "category":"misc",
    "alias":["ngap"],
    "exec": execute
}