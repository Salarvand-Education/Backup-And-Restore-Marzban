
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
 rm -r Backup-And-Restore-Marzban && git clone https://github.com/Salarvand-Education/Backup-And-Restore-Marzban.git && cd Backup-And-Restore-Marzban
    ```

2. Run the `run.sh` script and choose "1) Install the bot":

    ```sh
    chmod +x run.sh
    bash run.sh
    ```

3. Enter your bot token and admin chat ID when prompted.

## Update

To update the bot, run the `run.sh` script and choose "2) Update the bot":

```sh
bash run.sh
```

This will clone the repository again and run the bot.

## Removal

To remove the bot, run the `run.sh` script and choose "3) Remove the bot":

```sh
bash run.sh
```

This will delete the `Marzban-Backup-Restore` directory.

## Files

- `bot.py`: Main Telegram bot code.
- `run.sh`: Script for installing, updating, and removing the bot.
- `requirements.txt`: Python dependencies list.
- `.env`: Environment variables file (created by `run.sh`).

## Usage

After installing the bot, you can use the following commands in Telegram:

- `/start`: Start the bot and receive a welcome message.
- `/backup`: Backup the data.
- `/restore`: Restore the data (after sending the backup file).
- `/setinterval <minutes>`: Set the backup interval time.

Please note that the bot should be run on a Server with access to the Marzban paths.

