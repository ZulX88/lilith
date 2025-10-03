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
        
    menu = "🤖 *DAFTAR PERINTAH*\n\n"
    for cat in sorted(categorized):
        cat_title = cat.replace("_", " ").title()
        menu += f"🗂️ *{cat_title}*\n"
        for cmd in sorted(categorized[cat], key=lambda x: x["command"]):
            menu += f"• `{prefix}{cmd['command']}` → {cmd['name']}\n"
        menu += "\n"

    menu += "_Tip: Ketik .help <command> untuk detail_"
    await m.reply(menu)

plugin = {
    "command": "help",
    "name": "Bantuan",
    "category": "general",
    "alias": ["menu", "cmd"],
    "exec": execute
}