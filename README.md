<div align="center">

# 🤖 Discord Scheduled Channel Manager Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0+-blue.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Legacy%20Project-orange.svg)](#project-status)

*A Discord bot that automatically creates, manages, and schedules text channels based on time configurations. Perfect for temporary announcements, daily standup channels, or time-based community events.*

</div>

---

## ⚠️ Project Status

> **📍 Legacy Project Notice**  
> This is an **older project** that was developed some time ago. While it provides a solid foundation for Discord channel scheduling, **further development and modernization is needed** to bring it up to current standards. Contributions and improvements are welcome!

**Current State:**
- ✅ Basic functionality implemented
- ⚠️ May need updates for latest Discord.py versions
- 🔧 Code structure could benefit from refactoring
- 📚 Documentation could be expanded
- 🧪 Testing framework needs implementation

## ✨ Features

- 🕒 **Scheduled Channel Creation**: Automatically create channels at specified times daily
- 🗑️ **Automatic Channel Deletion**: Remove channels after a configurable duration
- 🔒 **Channel Locking**: Lock channels after a specified time to prevent further messages
- 👥 **Role-based Permissions**: Control who can access created channels
- 🌍 **Timezone Support**: Full timezone awareness for global servers
- 💾 **Database Persistence**: SQLite database for reliable data storage

## 📋 Commands

### 🎛️ `/scheduled_channel_create`
Create, show, or remove scheduled channel configurations.

**⚙️ Parameters:**
- 🔧 `action`: Set, Remove, or Show configurations
- 📁 `category`: Discord category where channels will be created
- ⏰ `daily_time`: Time to create the channel (12-hour format, e.g., "2:30 PM")
- ⏳ `delete_after`: How long before deleting the channel (e.g., "2h 30m")
- 🔐 `lock_after`: How long before locking the channel (e.g., "1h")
- 📝 `channel_name`: Name for the created channel
- 💬 `channel_text`: Initial message to post in the channel
- 👤 `channel_role`: Role that gets access to the channel

**🔑 Required Permissions:** Manage Server

## 🚀 Installation

### 📋 Prerequisites
- 🐍 Python 3.8 or higher
- 🤖 Discord Bot Token
- 🖥️ Server with appropriate bot permissions

### ⚡ Setup

1. **📥 Clone the repository:**
   ```bash
   git clone https://github.com/1ordo/discord-scheduled-channel-manager.git
   cd discord-scheduled-channel-manager
   ```

2. **📦 Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **🤖 Create a Discord Bot:**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application and bot
   - Copy the bot token

4. **⚙️ Configure environment variables:**
   Create a `configuration.env` file in the root directory:
   ```env
   BOT_TOKEN=your_discord_bot_token_here
   TIMEZONE=America/New_York
   ```

5. **🔗 Invite the bot to your server:**
   - Generate an invite link with the following permissions:
     - 👀 Read Messages
     - 💬 Send Messages
     - 🛠️ Manage Channels
     - 👁️ View Channels
     - 👥 Manage Roles (if using role-based permissions)

6. **▶️ Run the bot:**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### 🌐 Environment Variables

- 🔑 `BOT_TOKEN`: Your Discord bot token
- 🕐 `TIMEZONE`: Timezone for scheduling (e.g., "America/New_York", "Europe/London", "Asia/Tokyo")

### 💾 Database

The bot uses SQLite for data persistence. The database file (`system_data.db`) will be created automatically on first run.

## 💡 Usage Examples

### 📢 Daily Announcement Channel
Create a channel every day at 9:00 AM that deletes after 12 hours:
```
/scheduled_channel_create action:Set category:#announcements daily_time:"9:00 AM" delete_after:"12h" channel_name:"daily-updates" channel_text:"Good morning! Here are today's updates."
```

### 🎉 Temporary Event Channel
Create a channel for events that locks after 2 hours and deletes after 6 hours:
```
/scheduled_channel_create action:Set category:#events daily_time:"7:00 PM" delete_after:"6h" lock_after:"2h" channel_name:"evening-event" channel_text:"Tonight's event is starting!" channel_role:@EventMembers
```

## 📁 Project Structure

```
├── 🚀 main.py                 # Bot entry point
├── 🔧 client.py              # Discord client setup
├── ⚙️ configuration.py       # Environment configuration
├── 💾 database.py           # Database operations
├── 📋 requirements.txt      # Python dependencies
├── 📂 commands/
│   ├── 🎛️ channel_creation.py  # Channel management commands
│   └── 🔒 message_lock.py      # Message locking functionality
├── 📂 resources/
│   └── 🛡️ permissions.py       # Permission decorators
└── 📂 tasks/
    └── ⏰ time_check.py        # Scheduled task management
```

## 🤝 Contributing

> **💡 Help Needed!** This project would benefit from community contributions to modernize and improve it.

**Areas that need attention:**
- 🔄 Update to latest Discord.py version
- 🧪 Add comprehensive testing
- 📚 Improve documentation
- 🎨 Code refactoring and optimization
- 🔧 Add more configuration options
- 🐛 Bug fixes and improvements

**How to contribute:**
1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add some amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔀 Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. 🔍 Check the [Issues](https://github.com/1ordo/discord-scheduled-channel-manager/issues) page
2. 🐛 Create a new issue with detailed information about the problem

## 📝 Changelog

### Version 1.0.0
- 🎉 Initial release
- ⏰ Basic scheduled channel creation and deletion
- 👥 Role-based permissions
- 🌍 Timezone support
- 💾 Database persistence

---

<div align="center">

**⭐ If this project helped you, please consider giving it a star!**

*Made with ❤️ for the Discord community*

</div>
