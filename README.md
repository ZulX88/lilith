
<p align="center">
  <img src="files/lilith.jpg" alt="Lilith Logo" width="200"/>
</p>

<h1 align="center">🤖 Lilith</h1>

<p align="center">
  <strong>WhatsApp BOT based on Python with Asynchronous</strong>
</p>

<p align="center">
  <a href="https://github.com/ZulX88/Shiro-Py/stargazers">
    <img src="https://img.shields.io/github/stars/ZulX88/Shiro-Py?style=flat-square" alt="GitHub stars">
  </a>
  <a href="https://github.com/ZulX88/Shiro-Py/issues">
    <img src="https://img.shields.io/github/issues/ZulX88/Shiro-Py?style=flat-square" alt="GitHub issues">
  </a>
  <a href="https://github.com/ZulX88/Shiro-Py/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/ZulX88/Shiro-Py?style=flat-square" alt="GitHub">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat-square" alt="Python">
  </a>
</p>

---

## 🌟 About Lilith

Lilith is a powerful and easy-to-use WhatsApp bot, built with Python using asynchronous technology for optimal performance. With various exciting features, this bot is ready to assist your automation needs on WhatsApp.

### ✨ Main Features
- 🚀 **High Performance** - Utilizes asynchronous programming
- 🔧 **Easy to Customize** - Clean and modular code structure
- 📱 **WhatsApp Integration** - Directly connects with your WhatsApp account
- ⚡ **Responsive** - Fast response time for the best user experience
- 📥 **Media Handling** - Advanced media processing with `serialize.py` module
- 🔐 **Configuration Management** - Secure settings with `.env` support
- 📊 **Database Support** - SQLite and PostgreSQL integration

---

## 📚 Core Modules

### Message Serialization (`lib/serialize.py`)
The `serialize.py` module provides powerful message handling capabilities:

- **Mess Class**: Handles incoming messages with properties like:
  - `text`: Extracts message text content
  - `is_media`: Checks if the message contains media
  - `quoted`: Access to quoted/replied messages
  - `mentioned_jid`: Gets mentioned user IDs
  - `media_info`: Extracts detailed media information
  - `reply()`: Reply to messages
  - `react()`: React to messages with emojis

- **QuotedMess Class**: Handles quoted/replied messages with:
  - Media download capabilities
  - Context information extraction
  - Message type detection

## 📚 Documentation

Not familiar with the modules? Read the complete documentation here:
[📖 Official Documentation](https://nubuki-all.github.io/neonize)

**Special thanks to @Nubuki-all for the amazing documentation!** 🙏

---

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ZulX88/Shiro-Py.git
   cd Shiro-Py
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎯 How to Use

### 1. Generate Session
First, create your bot session:

```bash
python3 gen.py
```

Follow the instructions that appear to connect with your WhatsApp.

### 2. Running the Bot
Once the session is created, run the bot with:

```bash 
python3 -m main
```

The bot will be active and ready to use!

---

## 🛠️ System Requirements

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Quick Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit the .env file with your configurations
   ```

3. **Initialize Database**
   The bot will automatically create the database file specified in `NAMEDB`

## 🛠️ Configuration

Before running Lilith, you need to configure your `.env` file based on `.env.example`:

```env
PREFIXES=/
NAMEDB=db.sqlite3
OWNER=62xxx,84xxx
BOT_NAME=Lilith Bot
```

### Configuration Options:
- **PREFIXES**: Command prefixes for the bot (comma-separated values)
- **NAMEDB**: Database file name (supports SQLite or PostgreSQL connection string)
- **OWNER**: Owner number (comma-separated values) 
- **BOT_NAME**: Display name for the bot

---

## 🤝 Contribution

We highly welcome your contributions! To contribute:

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙋‍♂️ Support

If you like the Lilith project, consider:

- ⭐ Starring it on GitHub
- 🔄 Sharing it with friends
- ☕ Buy me a [coffee](https://saweria.co/zhansetya)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/ZulX88">ZulX88</a>
</p>
