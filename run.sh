#!/bin/bash

# Exit on any error
set -e

# Print commands and their arguments as they are executed
set -x

# Function to create .env file
create_env_file() {
    echo "Creating .env file..."
    read -p "Enter your Bot Token: " BOT_TOKEN
    read -p "Enter your Admin Chat ID: " ADMIN_CHAT_ID

    echo "BOT_TOKEN=$BOT_TOKEN" > .env
    echo "ADMIN_CHAT_ID=$ADMIN_CHAT_ID" >> .env
    echo ".env file created."
}

# Function to install the bot
install_bot() {
    echo "Installing the bot..."
    mkdir -p Marzban-Backup-Restore
    cd Marzban-Backup-Restore
    git clone https://github.com/Salarvand-Education/Backup-And-Restore-Marzban.git
    cd Backup-And-Restore-Marzban
    create_env_file
    pip install -r requirements.txt
    echo "Bot installed. You can now run it using 'python bot.py'"
}

# Function to update the bot
update_bot() {
    echo "Updating the bot..."
    rm -rf Marzban-Backup-Restore
    mkdir -p Marzban-Backup-Restore
    cd Marzban-Backup-Restore
    git clone https://github.com/Salarvand-Education/Backup-And-Restore-Marzban.git
    cd Backup-And-Restore-Marzban
    echo "Bot updated. Running the bot now..."
    nohup python bot.py &
}

# Function to remove the bot
remove_bot() {
    echo "Removing the bot..."
    rm -rf Marzban-Backup-Restore
    echo "Bot removed."
}

# Main menu
echo "Choose an option:"
echo "1) Install the bot"
echo "2) Update the bot"
echo "3) Remove the bot"
read -p "Enter the option number: " OPTION

case $OPTION in
    1)
        install_bot
        ;;
    2)
        update_bot
        ;;
    3)
        remove_bot
        ;;
    *)
        echo "Invalid option."
        ;;
esac
