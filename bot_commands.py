# bot_commands.py
import logging
import time
import os
import base64
import subprocess
from dotenv import load_dotenv
from telegram import Update, InputMediaPhoto
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from helpers import get_image_url, call_fooocus_async, get_job_status, progress_bar, check_endpoint, call_fooocus, call_whisper
from db import add_user_history_record_pg

# Load API configuration from environment variables
load_dotenv()
FOOOCUS_IP = os.getenv("FOOOCUS_IP")
ADMIN_ID = os.getenv("ADMIN_ID")
GROUP_ID = os.getenv("GROUP_ID")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # help message
    help_message = "just type /async <your prompt> to generate image\n"
    await update.message.reply_text(help_message)
    

async def make(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(".........make.........")
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
    
    print(".........create_image.........")
    print(update)                                              
    if update.message.chat.id not in [int(GROUP_ID), int(ADMIN_ID), -1002122545639, -1001772550506]:
        await update.message.reply_text("Sorry, you can't use this bot")
        return
    
    if check_endpoint() is not True:
        await update.message.reply_text("Sorry, service under maintenence :(")
        return
    
    # Removing "/make" from the string
    result = update.message.text.replace("/async", "").strip()
    
    text_identifier = await update.message.reply_text("Starting generate...")

    job_id = await call_fooocus_async(result, "Speed")
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
        except Exception as e:
            logging.error("Unhandled job_status exception: %s", e)

        time.sleep(1)
        job_status = await get_job_status(job_id)

    await image_identifier.delete()
    await text_identifier.delete()
    result_image = job_status["job_result"][0]["url"].replace("127.0.0.1", FOOOCUS_IP)

    file_path = await get_image_url(result_image)
    await update.message.reply_photo(file_path)
    
    # image to base64 string
    with open(file_path, 'rb') as file:  # 'rb' for reading in binary mode
        image_data = base64.b64encode(file.read())
    
    try:
        logging.info("starting DB insert")
        add_user_history_record_pg(update.effective_user.id, result, image_data)
    except Exception as e:
        logging.error("Unhandled database exception: %s", e)


async def audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the 'audio' command. Downloads an audio file and processes it.

    Parameters:
    update (Update): The update object containing the message.
    context (ContextTypes.DEFAULT_TYPE): The context object containing the bot and the current chat.

    Returns:
    None
    """
    logging.info(".........audio.........")
    # logging.info(update)

    if update.message.document is not None:
        file_name = update.message.document.file_name
        file = await context.bot.get_file(update.message.document)
    else:
        file_name = update.message.audio.file_name
        file = await context.bot.get_file(update.message.audio.file_id)
    
    await file.download_to_drive(f"tmp/{file_name}")
    
    # Run ffmpeg command
    formatted_file_name = f"tmp/{file_name.split('.')[0]}-formatted.wav"
    # await run_ffmpeg(file_name, formatted_file_name)
    
    subprocess.run(["ffmpeg", "-loglevel", "0", "-y", "-i", f"tmp/{file_name}", "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", formatted_file_name])

    result_text = await call_whisper(f"{formatted_file_name}")
    await update.message.reply_text(f'result: {result_text}')


def setup_handlers(app):
    app.add_handler(CommandHandler("make", make))
    app.add_handler(CommandHandler("async", make_async))
    app.add_handler(CommandHandler("help", help))
    # app.add_handler(CommandHandler("audio", audio))
    app.add_handler(MessageHandler(filters.ALL, audio))
    
    # Add other command handlers here
