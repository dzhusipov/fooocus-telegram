import shutil
import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import os


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


async def call_fooocus(prompt, performance):
    logging.info("Calling fooocus with prompt: " + prompt)
    url = "http://100.71.129.59:8888/v1/generation/text-to-image"
    # url = "http://192.168.1.42:8888/v1/generation/text-to-image"
    # performance = "Quality"
    # performance = "Speed"
    # performance = "Balanced"
    data = {
              "prompt": prompt,
              "negative_prompt": "",
              "style_selections": [
                "Fooocus V2",
                "Fooocus Enhance",
                "Fooocus Sharp"
              ],
              "performance_selection": performance,
              "aspect_ratios_selection": "1152*896",
              "image_number": 1,
              "image_seed": -1,
              "sharpness": 2,
              "guidance_scale": 4,
              "base_model_name": "juggernautXL_version6Rundiffusion.safetensors",
              "refiner_model_name": "None",
              "refiner_switch": 0.5,
              "loras": [
                {
                  "model_name": "sd_xl_offset_example-lora_1.0.safetensors",
                  "weight": 0.1
                }
              ],
              "advanced_params": {
                "adaptive_cfg": 7,
                "adm_scaler_end": 0.3,
                "adm_scaler_negative": 0.8,
                "adm_scaler_positive": 1.5,
                "canny_high_threshold": 128,
                "canny_low_threshold": 64,
                "controlnet_softness": 0.25,
                "debugging_cn_preprocessor": False,
                "debugging_inpaint_preprocessor": False,
                "disable_preview": False,
                "freeu_b1": 1.01,
                "freeu_b2": 1.02,
                "freeu_enabled": False,
                "freeu_s1": 0.99,
                "freeu_s2": 0.95,
                "inpaint_disable_initial_latent": False,
                "inpaint_engine": "v1",
                "inpaint_respective_field": 1,
                "inpaint_strength": 1,
                "mixing_image_prompt_and_inpaint": False,
                "mixing_image_prompt_and_vary_upscale": False,
                "overwrite_height": -1,
                "overwrite_step": -1,
                "overwrite_switch": -1,
                "overwrite_upscale_strength": -1,
                "overwrite_vary_strength": -1,
                "overwrite_width": -1,
                "refiner_swap_method": "joint",
                "sampler_name": "dpmpp_2m_sde_gpu",
                "scheduler_name": "karras",
                "skipping_cn_preprocessor": False
              },
              "require_base64": False,
              "async_process": False,
              "webhook_url": "string"
            }
    response = requests.post(url, json=data)
    logging.info(response.json())

    image_url = response.json()[0]['url'].replace("127.0.0.1", "100.71.129.59")
    # download image by url to tmp folder
    return image_url


async def get_image_url(image_url):
    response = requests.get(image_url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Define the temp directory path
        temp_dir = os.path.join(os.getcwd(), "tmp")

        # Create the temp directory if it doesn't exist
        os.makedirs(temp_dir, exist_ok=True)

        # Extracting the file name
        file_name = image_url.split('/')[-1]

        file_path = os.path.join(temp_dir, file_name)

        # Write the image to the file
        with open(file_path, 'wb') as out_file:
            response.raw.decode_content = True  # Ensure the complete image is downloaded
            shutil.copyfileobj(response.raw, out_file)

        logging.info(f"Image successfully downloaded to {file_path}")

        # print(f"Image successfully downloaded to {file_path}")
        return "tmp/" + file_name
    else:
        logging.error(f"Failed to retrieve the image. Status code: {response.status_code}")
        return "error"


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def make(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Removing "/make" from the string
    result = update.message.text.replace("/make", "").strip()
    await update.message.reply_text(f'Starting generate image with prompt: {result}')
    done_url = await call_fooocus(result, "Speed")
    file = await get_image_url(done_url)
    await update.message.reply_photo(file)


app = ApplicationBuilder().token("6778017668:AAEO_z45JQkygK1T8_J8e98GeBTSnOqFaAI").build()


# app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("make", make))

app.run_polling()
