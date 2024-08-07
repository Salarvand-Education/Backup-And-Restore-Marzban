
# Marzban Backup and Restore Bot

This project includes a Telegram bot used for backing up and restoring Marzban data.

## Prerequisites

- Python 3.x
- pip (Python package installer)
- Git

## Installation

To install the bot, follow these steps:

 1. Clone the repository and navigate to the project directory:

 ```sh
 git clone https://github.com/Salarvand-Education/Backup-And-Restore-Marzban.git && cd Backup-And-Restore-Marzban && chmod +x run.sh && bash run.sh
 ```

 2. Enter your bot token and admin chat ID when prompted.

## Files

- `bot.py`: Main Telegram bot code.
- `run.sh`: Script for installing the bot.
- `requirements.txt`: Python dependencies list.
- `.env`: Environment variables file (created by `run.sh`).

## Usage

After installing the bot, you can use the following commands in Telegram:

- `/start`: Start the bot and receive a welcome message.
- `/backup`: Backup the data.
- `/restore`: Restore the data (after sending the backup file).
- `/setinterval <minutes>`: Set the backup interval time.

Please note that the bot should be run on a Server with access to the Marzban paths.

