import os
import psycopg2
from dotenv import load_dotenv
import logging


def add_user_history_record_pg(chat_id, user_prompt, result_image):
    # Connect to PostgreSQL database
    conn = psycopg2.connect(**db_config())
    cursor = conn.cursor()

    # Insert a new record
    cursor.execute("INSERT INTO user_history (chat_id, user_prompt, result_image) VALUES (%s, %s, %s)", 
                   (chat_id, user_prompt, result_image))

    # Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    logging.info("Saved in DB")


def db_config():
    load_dotenv()
    return {
        'dbname': os.getenv("PG_DB"),
        'user': os.getenv("PG_USER"),
        'password': os.getenv("PG_PASS"),
        'host': os.getenv("PG_HOST")
    }
    
    
# Usage example
# db_config = {
#     'dbname': 'your_dbname',
#     'user': 'your_username',
#     'password': 'your_password',
#     'host': 'your_host'
# }
# add_user_history_record_pg(db_config, 'chat123', 'Hello, world!', image_data)
