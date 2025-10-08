# EscortBot - Telegram Bot for Home Server Monitoring

## 🚀 Overview
Telegram bot for monitoring home server services. Currently supports SSH connection monitoring with real-time alerts.

## 📋 Requirements
- Python 3.12+
- Linux system
- Dependencies: see `requirements.txt`

## 🤖 Getting the chat id
1. Create a bot via @BotFather in Telegram.
2. When filling in the config.conf file, create and leave the **chat_id** field empty.
3. Launch the bot and get your chat ID by sending `/start` to the bot.

## 🔧 Configuration
Configuration file - `config.conf`
When filling in the `config.conf` file, you can use both environment variables inside linux and from the .env file.
If you do not want to use environment variables, then enter the parameter values instead.

### For example
```ini
bot_token ESCORT_TELEGRAM_BOT_TOKEN          # Via service variables
bot_token 123456789:AAAbbbCccDddEeeFffGggHhh # Entering values directly
```

## 🚦 Usage
Launch file TelegramBot_for_HomeServer.py

## 📝 Logs
- Output to the console + write to a file
- Default log file: `escort.log` in the program directory
- The logging level is configured in config.conf `debug_level`

## 📄 License
MIT License - see LICENSE file