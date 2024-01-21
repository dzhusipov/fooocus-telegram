# bot_commands.py
import logging
import time
import os
import base64
from dotenv import load_dotenv
from telegram import Update, InputMediaPhoto
from telegram.ext import CommandHandler, ContextTypes
from helpers import get_image_url, call_fooocus_async, get_job_status, progress_bar

# Load API configuration from environment variables
load_dotenv()
FOOOCUS_IP = os.getenv("FOOOCUS_IP")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def make(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Removing "/make" from the string
    result = update.message.text.replace("/make", "").strip()
    identifier = await update.message.reply_text("Starting generate...")

    await identifier.edit_text(f'Generating image with prompt: {result}')
    done_url = await call_fooocus(result, "Speed")
    file = await get_image_url(done_url)
    await update.message.reply_photo(file)
    # await create_image(update, context)


async def make_async(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await create_image(update, context)


async def create_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Removing "/make" from the string
    result = update.message.text.replace("/async", "").strip()
    text_identifier = await update.message.reply_text("Starting generate...")

    job_id = await call_fooocus_async(result, "Quality")
    job_status = await get_job_status(job_id)
    image_identifier = None

    while job_status["job_stage"] == "RUNNING" or job_status["job_stage"] == "WAITING":
        try:
            if job_status["job_stage"] == "RUNNING" and job_status["job_step_preview"] is not None:
                if image_identifier is None:
                    image_identifier = await update.message.reply_photo(base64.b64decode(job_status["job_step_preview"]))
                else:
                    # remove old image
                    new_media = InputMediaPhoto(media=base64.b64decode(job_status["job_step_preview"]))
                    await image_identifier.edit_media(media=new_media)

                # await text_identifier.edit_text(f'Job progress: {job_progress}%')
                await text_identifier.edit_text(f'{progress_bar(job_status["job_progress"])}')
        except Exception:
            logging.error("Unhandled exception")
        
        time.sleep(1)
        job_status = await get_job_status(job_id)

    await image_identifier.delete()
    await text_identifier.delete()
    result_image = job_status["job_result"][0]["url"].replace("127.0.0.1", FOOOCUS_IP)

    file = await get_image_url(result_image)
    await update.message.reply_photo(file)
    

def setup_handlers(app):
    app.add_handler(CommandHandler("make", make))
    app.add_handler(CommandHandler("async", make_async))
    # Add other command handlers here
