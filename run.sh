#!/bin/bash

# Exit on any error
set -e

# Function to create .env file
create_env_file() {
    echo "Creating .env file..."
    read -p "Enter your Bot Token: " BOT_TOKEN
    read -p "Enter your Admin Chat ID: " ADMIN_CHAT_ID

    echo "BOT_TOKEN=$BOT_TOKEN" > .env
    echo "ADMIN_CHAT_ID=$ADMIN_CHAT_ID" >> .env
    echo ".env file created."
}

# Function to create systemd service file
create_systemd_service() {
    echo "Creating systemd service..."
    SERVICE_FILE="/etc/systemd/system/marzban-backup-restore.service"
    sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Marzban Backup and Restore Bot
After=network.target

[Service]
WorkingDirectory=/rootMarzban-Backup-Restore/Backup-And-Restore-Marzban
ExecStart=/usr/bin/python3 /rootMarzban-Backup-Restore/Backup-And-Restore-Marzban/bot.py
Restart=always
User=your_user
EnvironmentFile=/root/Marzban-Backup-Restore/Backup-And-Restore-Marzban/.env

[Install]
WantedBy=multi-user.target
EOL
    sudo systemctl daemon-reload
    sudo systemctl enable marzban-backup-restore.service
    sudo systemctl start marzban-backup-restore.service
    echo "Systemd service created and started."
}

# Function to install the bot
install_bot() {
    echo "Installing the bot..."
    git clone https://github.com/Salarvand-Education/Backup-And-Restore-Marzban.git
    cd Backup-And-Restore-Marzban
    create_env_file
    pip install -r requirements.txt
    create_systemd_service
    echo "Bot installed."
}

# Function to update the bot
update_bot() {
    echo "Updating the bot..."
    cd Marzban-Backup-Restore
    sudo systemctl stop marzban-backup-restore.service
    rm -rf Backup-And-Restore-Marzban
    git clone https://github.com/Salarvand-Education/Backup-And-Restore-Marzban.git
    cd Backup-And-Restore-Marzban
    echo "Bot updated. Running the bot now..."
    sudo systemctl start marzban-backup-restore.service
}

# Function to remove the bot
remove_bot() {
    echo "Removing the bot..."
    sudo systemctl stop marzban-backup-restore.service
    sudo systemctl disable marzban-backup-restore.service
    sudo rm /etc/systemd/system/marzban-backup-restore.service
    sudo systemctl daemon-reload
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
