# plugins/general/help.py

async def execute(client, m, prefix, **kwargs):
    try:
        if kwargs.get("command") not in ["help", "menu", "bantu", "list"]:
            return False

        try:
            text_body = m.text or m.caption or ""
            parts = text_body.split()
            query_cat = parts[1].lower() if len(parts) > 1 else None
        except Exception:
            query_cat = None

        seen = set()
        categorized = {}

        for cmd_data in client.command_plugins.values():
            main_cmd = cmd_data["command"].lower()
            if main_cmd in seen:
                continue
            seen.add(main_cmd)

            cat = cmd_data.get("category", "uncategorized").upper()
            if cat not in categorized:
                categorized[cat] = []
            categorized[cat].append(cmd_data)

        menu = ""

        if query_cat:
            target_cat = query_cat.upper()

            if target_cat in categorized:
                cat_title = target_cat.replace("_", " ")

                menu += f"✦ *{cat_title}* ✦\n"
                menu += f"_(⁠≧⁠▽⁠≦⁠) Ini dia isinya:_\n\n"

                for cmd in sorted(categorized[target_cat], key=lambda x: x["command"]):
                    menu += f"  ∘ `{prefix}{cmd['command']}` — {cmd['name']}\n"

                menu += "\n_Enjoy!_"

            else:
                menu += f"Hah? Kategori *{query_cat}* ga ada cik (⁠ ⁠･ั⁠﹏⁠･ั⁠)\n"
                menu += f"Coba cek lagi pakai `{prefix}menu`"

        else:
            menu += f"Hai! Mau butuh apa? (⁠≧⁠▽⁠≦⁠)\n"
            menu += f"━━━━━━━━━━━━━━━━\n"
            menu += f"*DAFTAR KATEGORI MENU*\n\n"

            for cat in sorted(categorized):
                pretty_cat = cat.lower()
                menu += f"  › `{prefix}menu {pretty_cat}`\n"

            menu += f"\n━━━━━━━━━━━━━━━━\n"
            menu += f" _Ketik salah satu command di atas ya!_"

        await client.send_image(m.chat, "files/lilith.jpg", caption=menu)
    except Exception as e:
        await m.reply(f"❌ Error: {str(e)}")

plugin = {
    "command": "help",
    "name": "Bantuan",
    "category": "general",
    "alias": ["menu", "cmd"],
    "exec": execute
}
