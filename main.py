# main.py
import logging
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from bot_commands import setup_handlers

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN set in .env file")

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

# Create and run the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
setup_handlers(app)
app.run_polling()
