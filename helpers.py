# helpers.py
import os
import shutil
import requests
import logging
from dotenv import load_dotenv
# import uuid
# import json
# import pika


# Load API configuration from environment variables
load_dotenv()
FOOOCUS_IP = os.getenv("FOOOCUS_IP")
FOOOCUS_PORT = os.getenv("FOOOCUS_PORT")
FOOOCUS_URL = f"http://{FOOOCUS_IP}:{FOOOCUS_PORT}/v1/generation/"
GENERATE_IMAGE_URI = "text-to-image"
GET_JOB_STATUS_URI = "query-job"

WHISPER_IP = os.getenv("WHISPER_IP")
WHISPER_PORT = os.getenv("WHISPER_PORT")

ADMIN_IP = os.getenv("ADMIN_ID")
GROUP_ID = os.getenv("GROUP_ID")


def return_data(prompt, performance, async_process):
    """
    Returns a dictionary with the provided parameters.

    Parameters:
    prompt (str): The prompt for the image generation.
    performance (str): The performance selection ("Quality", "Speed", "Balanced").
    async_process (bool): Whether the process should be asynchronous.

    Returns:
    dict: A dictionary containing the provided parameters.
    """
    data = {
        "prompt": prompt,
        "performance_selection": performance,
        "require_base64": False,
        "async_process": async_process,
        "webhook_url": "string"
    }
    return data


async def get_image_url(image_url):
    """
    Downloads an image from a given URL and saves it to a temporary directory.

    Parameters:
    image_url (str): The URL of the image to download.

    Returns:
    str: The path to the downloaded image, or "error" if the download failed.
    """
    response = requests.get(image_url, stream=True, timeout=30)
    if response.status_code == 200:
        temp_dir = os.path.join(os.getcwd(), "tmp")
        os.makedirs(temp_dir, exist_ok=True)
        file_name = image_url.split('/')[-1]
        file_path = os.path.join(temp_dir, file_name)

        with open(file_path, 'wb') as out_file:
            response.raw.decode_content = True  # Ensure the complete image is downloaded
            shutil.copyfileobj(response.raw, out_file)

        logging.info("Image successfully downloaded to %s", file_path)
        return "tmp/" + file_name
    else:
        logging.error("Failed to retrieve the image. Status code: {response.status_code}")
        return "error"
    

async def call_fooocus_async(prompt, performance):
    logging.info("Calling fooocus async with prompt: {prompt}")
    # task_id = str(uuid.uuid4())
    
    # # performance = "Quality" || "Speed" || "Balanced"
    data = return_data(prompt, performance, True)
    response = requests.post(FOOOCUS_URL + GENERATE_IMAGE_URI, json=data, timeout=30)
    # logging.info(response.json())
    job_id = response.json()['job_id']
    # download image by url to tmp folder
    return job_id
    
    # # Create your message with the task_id
    # message = {
    #     'task_id': task_id,
    #     'data' : data
    # }

    # # Send the task to RabbitMQ
    # channel.basic_publish(
    #     exchange='',
    #     routing_key='task_queue',
    #     body=json.dumps(message),
    #     properties=pika.BasicProperties(
    #         delivery_mode=2,  # make message persistent
    #     ))
    # logging.info("[x] Sent {message} to RabbitMQ with Task ID: {task_id}")
    # return task_id  # returning Task ID for future reference


async def call_fooocus(prompt, performance):
    logging.info("Calling fooocus with prompt: {prompt}")
    # performance = "Quality" || "Speed" || "Balanced"
    data = return_data(prompt, performance, False)
    response = requests.post(FOOOCUS_URL + GENERATE_IMAGE_URI, json=data, timeout=30)
    logging.info(response.json())

    image_url = response.json()[0]['url'].replace("127.0.0.1", FOOOCUS_IP)
    # download image by url to tmp folder
    return image_url


async def get_job_status(job_id):
    url = FOOOCUS_URL + GET_JOB_STATUS_URI
    print(url)
    params = {
        'job_id': job_id,
        'require_step_preview': True
    }

    response = requests.get(url, params=params, timeout=30)
    logging.info(response.json()["job_stage"])
    return response.json()


def progress_bar(percentage):
    max_length = 10  # Define the length of the progress bar
    filled_length = int(max_length * percentage // 100)  # Calculate filled length
    bar_of_the_progress = '█' * filled_length + '-' * (max_length - filled_length)  # Create the bar
    return f"[{bar_of_the_progress}] {percentage}%"


async def call_whisper(file_path):
    url = f"http://{WHISPER_IP}:{WHISPER_PORT}/whisper"
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files, timeout=60*10)
    logging.info( response.status_code )
    
    if response.status_code == 500:
        return "Server side error!"
    
    # return "test"
    json_reposnse = response.json()
    return json_reposnse["results"][0]["transcript"]


def check_endpoint():
    try:
        response = requests.get(f"http://{FOOOCUS_IP}:{FOOOCUS_PORT}/ping", timeout=5)
        return response.text == "pong"
    except requests.RequestException:
        return False
