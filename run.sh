#!/bin/bash

# Prompting the user for the bot token and admin chat ID
read -p "Please enter your bot token: " BOT_TOKEN
read -p "Please enter your admin chat ID: " ADMIN_CHAT_ID

# Creating or overwriting the .env file
cat <<EOL > .env
BOT_TOKEN=$BOT_TOKEN
ADMIN_CHAT_ID=$ADMIN_CHAT_ID
EOL

echo "Information successfully saved to .env file."
pkill -f bot.py
# Running the Python script
nohup python3 bot.py &
