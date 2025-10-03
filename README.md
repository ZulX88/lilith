<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Architects+Daughter&size=40&duration=3000&pause=1000&color=F79F1F&center=true&vCenter=true&multiline=true&width=600&height=100&lines=A+whisper+between+protocols;ShiroPy2+A+Revolution+in+Bot+Development" alt="Typing SVG" />
</div>

<div align="center">
  <img src="files/lilith.jpg" alt="ShiroPy2 Logo" width="250" height="250" style="border-radius: 50%; border: 5px solid #F79F1F; box-shadow: 0 0 30px rgba(247, 159, 31, 0.7); animation: rotate 20s linear infinite;"/>
</div>

<style>
@keyframes rotate {
  0% { transform: rotate(0deg) scale(1); }
  50% { transform: rotate(180deg) scale(1.05); }
  100% { transform: rotate(360deg) scale(1); }
}
</style>

<h1 align="center">🤖 ShiroPy2 - Advanced Bot Framework </h1>

<p align="center">
  <em>A whisper between protocols - Advanced Bot Framework Built with Python & Asynchronous Technology</em>
</p>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=ZulX88&label=Repository%20Views&color=blueviolet&style=flat-square" alt="Repository Views" />
</p>

<div align="center">
  
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green?style=for-the-badge&logo=github)
![Python](https://img.shields.io/badge/Made%20with-Python-1f425f?style=for-the-badge&logo=python)
![License](https://img.shields.io/github/license/ZulX88/ShiroPy2?style=for-the-badge&logo=github&color=blue)
![Stars](https://img.shields.io/github/stars/ZulX88/ShiroPy2?style=for-the-badge&logo=github&color=f4db53)
![Issues](https://img.shields.io/github/issues/ZulX88/ShiroPy2?style=for-the-badge&logo=github&color=red)
![Forks](https://img.shields.io/github/forks/ZulX88/ShiroPy2?style=for-the-badge&logo=github&color=success)
![Contributors](https://img.shields.io/github/contributors/ZulX88/ShiroPy2?style=for-the-badge&logo=github&color=purple)

</div>

---

## 🌟 About ShiroPy2

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=20&duration=4000&pause=1000&color=00D17A&center=true&vCenter=true&repeat=false&width=600&height=30&lines=A+whisper+between+protocols" alt="About ShiroPy2" />
</div>

ShiroPy2 is an advanced bot framework meticulously crafted with Python and asynchronous technology for optimal performance. Designed to revolutionize your automation experience, this framework combines cutting-edge functionality with elegant design. A whisper between protocols, connecting you with seamless integration.

### ✨ Key Features

<div align="center">
  
<table>
  <tr>
    <td align="center" width="33%"><div><h3>🚀 Performance</h3></div></td>
    <td align="center" width="33%"><div><h3>🔧 Customization</h3></div></td>
    <td align="center" width="33%"><div><h3>📱 Integration</h3></div></td>
  </tr>
  <tr>
    <td align="center">Asynchronous architecture for lightning-fast responses</td>
    <td align="center">Modular design for easy customization</td>
    <td align="center">Seamless API integration</td>
  </tr>
  <tr>
    <td align="center" width="33%"><h3>⚡ Responsiveness</h3></td>
    <td align="center" width="33%"><h3>📥 Media Handling</h3></td>
    <td align="center" width="33%"><h3>🔐 Security</h3></td>
  </tr>
  <tr>
    <td align="center">Real-time processing with minimal latency</td>
    <td align="center">Advanced media processing capabilities</td>
    <td align="center">Secure environment configuration</td>
  </tr>
</table>

</div>

### <kbd>🎯</kbd> Core Capabilities

<div align="center">

| <kbd>💬</kbd> **Message Processing** | <kbd>📁</kbd> **Media Management** | <kbd>🗄️</kbd> **Database Integration** |
|:-----------------------------------:|:---------------------------------:|:-------------------------------------:|
| Sophisticated message parsing and handling | Advanced media upload and download capabilities | Robust SQLite and PostgreSQL support |

| <kbd>⚙️</kbd> **Event Handling** | <kbd>🔌</kbd> **Plugin System** | <kbd>🌐</kbd> **Protocol Whisper** |
|:------------------------------:|:------------------------------:|:-------------------------------:|
| Comprehensive event-driven architecture | Extensible plugin architecture for easy feature additions | A whisper between protocols for seamless communication |

</div>

---

## 📊 GitHub Stats

<div align="center">
  
![ZulX88's GitHub stats](https://github-readme-stats.vercel.app/api?username=ZulX88&show_icons=true&theme=radical&count_private=true)
  
</div>

<div align="center">
  
![GitHub Streak](https://github-readme-streak-stats.herokuapp.com/?user=ZulX88&theme=radical)
  
</div>

---

## 🏗️ Architecture Overview

### Core Components

<div align="center">
  
```mermaid
graph TD
    A[WhatsApp Client] --> B[Message Handler]
    B --> C[Command Parser]
    C --> D[Plugin System]
    D --> E[Database Layer]
    D --> F[Media Processor]
    D --> G[API Interfaces]
    B --> H[Event Manager]
```

</div>

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

<div align="center">
  
#### 🚀 Rapid Deployment
```bash
git clone https://github.com/ZulX88/ShiroPy2.git
cd ShiroPy2
pip install -r requirements.txt
```

</div>

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ZulX88/ShiroPy2.git
   cd ShiroPy2
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
  
### <kbd>⚙️</kbd> Environment Variables

<div align="center">
  
```env
PREFIXES=/
NAMEDB=db.sqlite3
OWNER=62xxx,84xxx
BOT_NAME=ShiroPy2 Bot
```

</div>

| <kbd>🔧</kbd> **Variable** | **Description** | **Example** |
|:--------------------------:|:---------------:|:-----------:|
| **PREFIXES** | Command prefixes for the bot | `/` |
| **NAMEDB** | Database file name | `db.sqlite3` |
| **OWNER** | Owner numbers (comma-separated) | `62xxx,84xxx` |
| **BOT_NAME** | Display name for the bot | `ShiroPy2 Bot` |

</div>

---

## 🗂️ Project Structure

<div align="center">
  
```
ShiroPy2/
├── main.py                 # 🖥️  Main framework entry point
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
  
### <kbd>🔌</kbd> Available Plugins

<table>
  <tr>
    <th>Plugin Category</th>
    <th>Functionality</th>
    <th>Status</th>
  </tr>
  <tr>
    <td align="center"><kbd>📥</kbd> <strong>Downloader</strong></td>
    <td>Media download capabilities</td>
    <td align="center">✅ <em>Active</em></td>
  </tr>
  <tr>
    <td align="center"><kbd>🧩</kbd> <strong>General</strong></td>
    <td>Basic bot commands</td>
    <td align="center">✅ <em>Active</em></td>
  </tr>
  <tr>
    <td align="center"><kbd>🎵</kbd> <strong>Music</strong></td>
    <td>Music search and download</td>
    <td align="center">🔄 <em>Coming Soon</em></td>
  </tr>
  <tr>
    <td align="center"><kbd>🤖</kbd> <strong>AI</strong></td>
    <td>Artificial intelligence features</td>
    <td align="center">🔄 <em>Coming Soon</em></td>
  </tr>
</table>

</div>

---

## 🤝 Contribution

<div align="center">
  
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](https://github.com/ZulX88/ShiroPy2/pulls)
[![Contributors](https://img.shields.io/github/contributors/ZulX88/ShiroPy2?style=for-the-badge&color=orange)](https://github.com/ZulX88/ShiroPy2/graphs/contributors)

</div>

We warmly welcome your contributions! To contribute:

1. **Fork** the repository
2. **Create** your feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

Join us in developing "A whisper between protocols" - making bot automation more elegant and efficient.

<div align="center">

### 🌟 Contributors
<a href="https://github.com/ZulX88/ShiroPy2/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ZulX88/ShiroPy2" alt="Contributors" />
</a>

</div>

---

## 📈 Activity Insights

<div align="center">
  
![GitHub Activity Graph](https://activity-graph.herokuapp.com/graph?username=ZulX88&theme=github)
  
</div>

---

## 🏆 Achievements

<div align="center">
  
![GitHub Trophies](https://github-profile-trophy.vercel.app/?username=ZulX88&theme=dracula&no-frame=true&margin-w=15&row=1)
  
</div>

---

## 🙏 Acknowledgments

<div align="center">
  
- Special thanks to [@Nubuki-all](https://github.com/Nubuki-all) for the [amazing documentation](https://nubuki-all.github.io/neonize)! 🙏
- Inspired by the open-source community and developers worldwide 💙
- Built with [neonize](https://github.com/krypton-byte/neonize) framework 🚀
- "A whisper between protocols" - connecting technologies seamlessly
</div>

</div>

---

## 📞 Connect with Me

<div align="center">
  
[<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">](https://github.com/ZulX88) 
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

<div align="center">
  
![Repo Support](https://repobeats.axiom.co/api/embed/0c8a1ff1540b3e116f4355e95c9e9d9c342f01e3.svg "Repobeats analytics image")

</div>

---

<div align="center">
  
### 🌟 Thank You for Visiting!

[![Stargazers repo roster for @ZulX88/ShiroPy2](https://reporoster.com/stars/ZulX88/ShiroPy2)](https://github.com/ZulX88/ShiroPy2/stargazers)
  
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
  Made with ❤️ by <a href="https://github.com/ZulX88">ZulX88</a> | 🤖 ShiroPy2 - A whisper between protocols
</p>