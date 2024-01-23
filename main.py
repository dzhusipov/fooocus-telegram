# main.py
import logging
import os
import threading
import time
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from bot_commands import setup_handlers


def clean_tmp_folder():
    while True:
        tmp_folder = 'tmp'  # Replace with your tmp folder path
        current_time = time.time()
        for file in os.listdir(tmp_folder):  # Iterate through files
            file_path = os.path.join(tmp_folder, file)
            file_mod_time = os.path.getmtime(file_path)
            if current_time - file_mod_time > 60*5:  # Check if file is older than 5 minutes
                os.remove(file_path)  # Delete the file
        time.sleep(60)  # Sleep for 1 minute


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
