# Marzban Backup & Restore Telegram Bot

This is a Telegram bot designed to backup and restore Marzban files and database. The bot can send backups to a specified Telegram chat and restore backups on command.

## Features

- Backup Marzban files and database.
- Send backups to a specified Telegram chat.
- Restore backups from a file sent via Telegram.
- Configurable backup interval.
- Uses a `.env` file to securely manage bot token and admin chat ID.

## Requirements

- Python 3.7+
- `python-dotenv` package
- `python-telegram-bot` package
- `schedule` package
- `nest_asyncio` package

## Installation

1. download and unzip and remove zip file and edit .env

    ```bash
     mkdir Backup-And-Restore && cd Backup-And-Restore &&wget https://raw.githubusercontent.com/Salarvand-Education/Backup-And-Restore-marzban/main/Backup-And-Restore.zip && unzip Backup-And-Restore.zip && rm -r Backup-And-Restore.zip && pip install -r requirements.txt && nano .env
    ```
2. Create a `.env` file in the root directory of the project and add your bot token and admin chat ID:

    ```bash
    BOT_TOKEN=your-bot-token
    ADMIN_CHAT_ID=your-admin-chat-id
    ```

3. Run the bot:

    ```bash
   nohup python3 bot.py &
    ```

## Usage

### Commands

- `/start`: Start the bot and receive a welcome message.
- `/backup`: Manually trigger a backup.
- `/restore`: Restore from a backup file sent via Telegram.
- `/setinterval <minutes>`: Set the backup interval in minutes.

### Backup & Restore Process

1. To manually trigger a backup, send the `/backup` command.
2. The bot will automatically send backups to the specified chat at the configured interval.
3. To restore from a backup, send the `/restore` command and then upload the backup file.
4. The bot will restore the Marzban files and database and notify you upon completion.

## Environment Variables

The bot uses a `.env` file to manage sensitive information. Create a `.env` file in the root directory and add the following variables:

```env
BOT_TOKEN=your-bot-token
ADMIN_CHAT_ID=your-admin-chat-id
