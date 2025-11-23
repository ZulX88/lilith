# plugins/general/help.py

async def execute(client, m, prefix, **kwargs):
    if kwargs.get("command") not in ["help", "menu", "bantu", "list"]:
        return False
        
    # --- 1. Parsing Input ---
    try:
        text_body = m.text or m.caption or ""
        parts = text_body.split()
        query_cat = parts[1].lower() if len(parts) > 1 else None
    except Exception:
        query_cat = None

    # --- 2. Grouping ---
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
    
    # --- 3. Tampilan Baru (Estetik No-Kotak) ---
    
    if query_cat:
        # === TAMPILAN ISI KATEGORI ===
        target_cat = query_cat.upper()
        
        if target_cat in categorized:
            cat_title = target_cat.replace("_", " ")
            
            # Header Kategori
            menu += f"✦ *{cat_title}* ✦\n"
            menu += f"_(⁠≧⁠▽⁠≦⁠) Ini dia isinya:_\n\n"
            
            # List Command
            for cmd in sorted(categorized[target_cat], key=lambda x: x["command"]):
                # Style: ∘ .command — Nama/Desc
                menu += f"  ∘ `{prefix}{cmd['command']}` — {cmd['name']}\n"
                
            menu += "\n_Enjoy!_"
            
        else:
            # Error Message
            menu += f"Hah? Kategori *{query_cat}* ga ada cik (⁠≧⁠▽⁠≦⁠)\n"
            menu += f"Coba cek lagi pakai `{prefix}menu`"
            
    else:
        # === TAMPILAN DAFTAR KATEGORI ===
        menu += f"Hai! Mau butuh apa? (⁠≧⁠▽⁠≦⁠)\n"
        menu += f"━━━━━━━━━━━━━━━━\n"
        menu += f"*DAFTAR KATEGORI MENU*\n\n"
        
        for cat in sorted(categorized):
            pretty_cat = cat.lower()
            # Style: › menu kategori
            menu += f"  › `{prefix}menu {pretty_cat}`\n"
            
        menu += f"\n━━━━━━━━━━━━━━━━\n"
        menu += f" _Ketik salah satu command di atas ya!_"

    # Kirim hasil
    await client.send_image(m.chat, "files/lilith.jpg", caption=menu)

plugin = {
    "command": "help",
    "name": "Bantuan",
    "category": "general",
    "alias": ["menu", "cmd"],
    "exec": execute
}
