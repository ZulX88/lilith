from lib.scrape import pins

async def execx(client,m,text,**kwargs):
    try:
        if not text:
            return await m.reply("*Mau nyari foto apa?*")

        search_pins=await pins(text,limit=10)
        await m.react("🔎")
        container=[]

        for data in search_pins:
            if not data["image"].endswith(("jpg", "png", "jpeg")):
                continue
            payload={
                "image_url":data["image"],
                "body":{
                    "text":f"*Upload by*: {data['upload_by']}"
                },
                "buttons":[
                    {
                        "name":"cta_url",
                        "buttonParamsJSON":str(
                            {
                                "display_text":"Source",
                                "url":data["source"]
                            }
                        )
                    }
                ]
            }

            container.append(payload)

        await m.react("⏳")
        await client.send_carousel(m.chat,container,body=f"Ini kak")
        await m.react("✅")
    except Exception as e:
        await m.reply(f"❌ Error: {str(e)}")

plugin={
    "name":"Pinterest Search",
    "category":"search",
    "command":"pinterest",
    "alias":["pins","pin-search","pinterest-search","pin-s"],
    "exec":execx
}