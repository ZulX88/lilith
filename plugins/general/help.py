# plugins/general/help.py

async def execute(client, m, prefix, **kwargs):
    if kwargs.get("command") not in ["help", "menu", "bantu", "list"]:
        return False
        
    seen = set()
    categorized = {}
    
    for cmd_data in client.command_plugins.values():
        main_cmd = cmd_data["command"].lower()
        if main_cmd in seen:
            continue
        seen.add(main_cmd)

        cat = cmd_data.get("category", "uncategorized")
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append(cmd_data)
        
    # Header menu
    menu = "╔════════════════════════╗\n"
    menu += "║       🤖 LILITH BOT 🤖        ║\n"
    menu += "║      DAFTAR PERINTAH      ║\n"
    menu += "╚════════════════════════╝\n\n"
    
    # Menampilkan kategori dengan ikon dan format yang lebih menarik
    for cat in sorted(categorized):
        cat_title = cat.replace("_", " ").upper()
        menu += f"┌── 📚 *{cat_title}* ──┐\n"
        
        for cmd in sorted(categorized[cat], key=lambda x: x["command"]):
            menu += f"│ • `{prefix}{cmd['command']}`\n"
            menu += f"│   ↳ {cmd['name']}\n"
        
        menu += "└─────────────────────────┘\n\n"

    # Footer dengan nama bot
    from config import bot_name
    menu += f"✨ *{bot_name}*"
    
    # Kirim gambar dengan caption berisi menu
    await client.send_image(m.chat, "files/lilith.jpg", caption=menu)

plugin = {
    "command": "help",
    "name": "Bantuan",
    "category": "general",
    "alias": ["menu", "cmd"],
    "exec": execute
}