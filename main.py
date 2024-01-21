# main.py
import logging
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from bot_commands import setup_handlers
import threading
import time


def clean_tmp_folder():
    while True:
        tmp_folder = 'tmp'  # Replace with your tmp folder path
        os.chdir(tmp_folder)  # Step 1: Enter tmp folder
        for file in os.listdir():  # Step 2: Clear content of folder
            os.remove(file)
        os.chdir('..')  # Go back to the original directory
        time.sleep(60)  # Step 3: Sleep 60 seconds


load_dotenv()
# Load environment variables
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


# Start the cleaning thread
cleaning_thread = threading.Thread(target=clean_tmp_folder, daemon=True)
cleaning_thread.start()

# Create and run the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
setup_handlers(app)
app.run_polling()
