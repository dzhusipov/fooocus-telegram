# Telegram Bot for Fooocus
![alt img](https://raw.githubusercontent.com/dzhusipov/fooocus-telegram/master/img/LogoFooocusTelegrambot.png)
## Overview
This repository contains the code for a Python-based Telegram bot. This bot interacts with the Fooocus API to generate and preview images.

## Features
- 🤖 Telegram Bot Integration
- 🎨 Image Generation with Fooocus API
- 🔍 Image Preview Functionality

## Requirements
- Python 3.x
- Telegram Bot Token
- Fooocus API Key

## Installation
```bash
git clone git@github.com:dzhusipov/fooocus-telegram.git
cd fooocus-telegram
<<<<<<< HEAD
pip install requests python-telegram-bot python-dotenv
=======
pip install psycopg2 requests python-telegram-bot python-dotenv
>>>>>>> develop
```

## Usage
Set your Telegram Bot Token and Fooocus API Key in .env file:  
```bash
FOOOCUS_IP = 0.0.0.0
FOOOCUS_PORT = 8080
BOT_TOKEN = YOUR_BOT_TOKEN
ADMIN_ID = 123123123123
GROUP_ID = -123123123123123
# Database
PG_DB = postgres
PG_PASS = 1234567890
PG_USER = postgres
PG_HOST = localhost 
```

## Run the bot:
```bash
python main.py
```

## Contributing
Contributions, issues, and feature requests are welcome!  

## License
Distributed under the MIT License. See LICENSE.md for more information.  

## Contact
Telegram: @DrunkSausage  
