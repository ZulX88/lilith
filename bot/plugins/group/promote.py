from neonize.utils.enum import ParticipantChange

async def execute(client,m,text,**kwargs):
    target = (m.mentioned_jid[0] if m.mentioned_jid else None) \
         or (getattr(m, "quoted", None) and getattr(m.quoted, "sender", None)) \
         or text
    
    try:
        await client.update_group_participants(m.chat,[target],ParticipantChange.PROMOTE)
        await m.reply(f"✅ Successfully promoted {target.User}!")
    except Exception as e:
        await m.reply(f"❌ Failed to promote {target.User}: {str(e)}")
   
plugin={
    "name":"Promote member",
    "command":"promote",
    "category":"group",
    "admin":True,
    "botAdmin":True,
    "exec":execute
}