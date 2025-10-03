<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Architects+Daughter&size=40&duration=3000&pause=1000&color=FF0000&center=true&vCenter=true&multiline=true&width=600&height=100&lines=A+whisper+between+protocols" alt="Typing SVG" />
</div>

<br>

<div align="center">
  <img src="files/lilith.jpg" alt="Lilith Logo" width="200" height="200" style="border-radius: 50%; border: 4px solid #000000; box-shadow: 0 0 25px rgba(0, 0, 0, 0.7); margin: 20px 0;"/>
</div>

<h1 align="center">🤖 Lilith - WhatsApp Bot </h1>

<p align="center">
  <em style="color: #000000; background: linear-gradient(to right, #ff0000, #000000); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold;">A Cutting-Edge WhatsApp Bot Built with Python & Asynchronous Technology</em>
</p>



<p align="center">
  <img src="https://komarev.com/ghpvc/?username=ZulX88&label=Repository%20Views&color=blueviolet&style=flat-square" alt="Repository Views" />
</p>

<div align="center" style="background: linear-gradient(135deg, #000000 0%, #333333 50%, #ff0000 100%); padding: 15px; border-radius: 10px; margin: 15px 0;">

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-red.svg?style=for-the-badge)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![Python](https://img.shields.io/badge/Made%20with-Python-black.svg?style=for-the-badge)](https://www.python.org/)
[![License](https://img.shields.io/github/license/ZulX88/lilith?style=for-the-badge&logo=github&color=red)](https://github.com/ZulX88/lilith/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/ZulX88/lilith?style=for-the-badge&logo=github&color=white)](https://github.com/ZulX88/lilith/stargazers)
[![Issues](https://img.shields.io/github/issues/ZulX88/lilith?style=for-the-badge&logo=github&color=red)](https://github.com/ZulX88/lilith/issues)

</div>

---

## 🌟 About Lilith

Lilith is an advanced WhatsApp bot meticulously crafted with Python and asynchronous technology for optimal performance. Designed to revolutionize your WhatsApp automation experience, this bot combines cutting-edge functionality with elegant design.

### ✨ Key Features

<div align="center">
  
| 🚀 **Performance** | 🔧 **Customization** | 📱 **Integration** |
|:---:|:---:|:---:|
| Asynchronous architecture for lightning-fast responses | Modular design for easy customization | Seamless WhatsApp API integration |

| ⚡ **Responsiveness** | 📥 **Media Handling** | 🔐 **Security** |
|:---:|:---:|:---:|
| Real-time processing with minimal latency | Advanced media processing capabilities | Secure environment configuration |

</div>

### 🎯 Core Capabilities

- **Message Processing**: Sophisticated message parsing and handling
- **Media Management**: Advanced media upload and download capabilities  
- **Database Integration**: Robust SQLite and PostgreSQL support
- **Event Handling**: Comprehensive event-driven architecture
- **Plugin System**: Extensible plugin architecture for easy feature additions

---

## 📊 GitHub Stats

<div align="center">
  
![ZulX88's GitHub stats](https://github-readme-stats.vercel.app/api?username=ZulX88&show_icons=true&theme=radical&count_private=true)
  
</div>

<div align="center">
  
![GitHub Streak](https://github-readme-streak-stats.herokuapp.com/?user=ZulX88&theme=radical)
  
</div>

---

### Message Serialization (`lib/serialize.py`)

The `serialize.py` module provides powerful message handling capabilities:

#### **Mess Class**
Handles incoming messages with properties like:

- `text`: Extracts message text content
- `is_media`: Checks if the message contains media
- `quoted`: Access to quoted/replied messages
- `mentioned_jid`: Gets mentioned user IDs
- `media_info`: Extracts detailed media information
- `reply()`: Reply to messages
- `react()`: React to messages with emojis

#### **QuotedMess Class**
Handles quoted/replied messages with:

- Media download capabilities
- Context information extraction
- Message type detection

---

## 📚 Quick Start

<div align="center">
  
### Prerequisites
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![pip](https://img.shields.io/badge/pip-21.0%2B-blue?style=for-the-badge&logo=pip&logoColor=white)](https://pip.pypa.io/en/stable/)

</div>

### Installation

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ZulX88/lilith.git
   cd lilith
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

4. **Generate Session**
   ```bash
   python3 gen.py
   ```

5. **Run the Bot**
   ```bash
   python3 -m main
   ```

> ⚠️ **Note**: Follow the instructions that appear during session generation to connect with your WhatsApp.

---

## ⚙️ Configuration

<div align="center">
  
### Environment Variables
```env
PREFIXES=/
NAMEDB=db.sqlite3
OWNER=62xxx,84xxx
BOT_NAME=Lilith Bot
```

</div>

| Variable | Description | Default |
|----------|-------------|---------|
| **PREFIXES** | Command prefixes for the bot | `/` |
| **NAMEDB** | Database file name | `db.sqlite3` |
| **OWNER** | Owner numbers (comma-separated) | `62xxx,84xxx` |
| **BOT_NAME** | Display name for the bot | `Lilith Bot` |

---

## 🗂️ Project Structure

<div align="center">
  
```
lilith/
├── main.py                 # 🖥️  Main bot entry point
├── gen.py                  # 🔐  Session generation script  
├── handler.py              # 🤖  Message handler
├── config.py               # ⚙️  Configuration settings
├── requirements.txt        # 📦  Python dependencies
├── .env.example           # 🔐  Environment variables template
├── files/                 # 📁  Static files directory
├── lib/                   # 🧩  Core library modules
│   ├── serialize.py       # 📬  Message serialization
│   └── scrape/            # 🌐  Scraping utilities
└── plugins/               # 🔌  Bot plugins directory
    ├── downloader/        # 📥  Download plugins
    └── general/           # 🧩  General plugins
```

</div>

---

## 🧩 Available Plugins

<div align="center">
  
| Plugin Category | Functionality | Status |
|----------------|---------------|--------|
| 📥 **Downloader** | Media download capabilities | ✅ Active |
| 🧩 **General** | Basic bot commands | ✅ Active |
| 🎵 **Music** | Music search and download | 🔄 Coming Soon |
| 🤖 **AI** | Artificial intelligence features | 🔄 Coming Soon |

</div>

---

## 🤝 Contribution

<div align="center">
  
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](https://github.com/ZulX88/lilith/pulls)
[![Contributors](https://img.shields.io/github/contributors/ZulX88/lilith?style=for-the-badge&color=orange)](https://github.com/ZulX88/lilith/graphs/contributors)

</div>

We warmly welcome your contributions! To contribute:

1. **Fork** the repository
2. **Create** your feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

<div align="center">

### 🌟 Contributors
<a href="https://github.com/ZulX88/lilith/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ZulX88/lilith" alt="Contributors" />
</a>

</div>

---





## 🙏 Acknowledgments

<div align="center">
  
- Special thanks to [@Nubuki-all](https://github.com/Nubuki-all) for the [amazing documentation](https://nubuki-all.github.io/neonize)! 🙏
- Inspired by the open-source community and developers worldwide 💙
- Built with [neonize](https://github.com/krypton-byte/neonize) framework 🚀

</div>

</div>

---

## 📞 Connect with Me

<div align="center">
  
[<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">](https://github.com/ZulX88) 
[<img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">](https://t.me/ILoveLilith) 
[<img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter">](https://twitter.com/NaruseShirohaXZ) 
[<img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram">](https://instagram.com/zhann44n)

</div>

---

## 💰 Support the Project

<div align="center">
  
If you find Lilith useful, consider supporting the project:
  
[<img src="https://img.shields.io/badge/Saweria-FFA500?style=for-the-badge&logo=Buy+Me+A+Coffee&logoColor=white" alt="Saweria">](https://saweria.co/zhansetya)
[<img src="https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white" alt="Ko-fi">](https://ko-fi.com/zhansetya)

</div>



---

<div align="center">
  
### 🌟 Thank You for Visiting!

[![Stargazers repo roster for @ZulX88/lilith](https://reporoster.com/stars/ZulX88/lilith)](https://github.com/ZulX88/lilith/stargazers)
  
</div>

<div align="center">
  
<a href="#top">
  <img src="https://img.shields.io/badge/Back%20to%20Top-000000?style=for-the-badge&logo=github&logoColor=white" alt="Back to Top">
</a>

</div>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer" alt="Wave Generator" />
</p>

</div>
</div>

<p align="center">
  Made with ❤️ by <a href="https://github.com/ZulX88">ZulX88</a> | 🤖 Lilith Bot - Your Ultimate WhatsApp Assistant
</p>
