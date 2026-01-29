import time
from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import Message

async def execute(client, m, **kwargs):
    try:
        start = time.time()
        msg = await m.reply("🏓 Pong!")
        end = time.time()
        latency = (end - start) * 1000 
        await client.edit_message(m.chat, msg.ID, Message(conversation=f"🏓 Pong!\n*Result* : {latency:.2f}ms"))
    except Exception as e:
        await m.reply(f"❌ Error: {str(e)}")

plugin = {
    "command": "ping",
    "name": "Ping Bot",
    "category": "general",
    "alias": ["ngap"],
    "exec": execute
}