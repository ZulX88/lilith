from neonize.utils.enum import ParticipantChange

async def execute(client,m,text,**kwargs):
    target = (m.mentioned_jid[0] if m.mentioned_jid else None) \
         or (getattr(m, "quoted", None) and getattr(m.quoted, "sender", None)) \
         or text
    
    try:
        await client.update_group_participants(m.chat,[target],ParticipantChange.ADD)
        await m.reply(f"✅ Successfully added {target.User} to the group!")
    except Exception as e:
        await m.reply(f"❌ Failed to add {target.User} to the group: {str(e)}")
   
plugin={
    "name":"Add member",
    "command":"add",
    "category":"group",
    "owner":True,
    "botAdmin":True,
    "exec":execute
}