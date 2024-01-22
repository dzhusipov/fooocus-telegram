import sqlite3
from dotenv import load_dotenv
import os


def add_user_history_record(chat_id, user_prompt, result_image):
    # Connect to SQLite database
    load_dotenv()
    db_path = os.getenv("DB_PATH")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert a new record
    cursor.execute("INSERT INTO user_history (chat_id, user_prompt, result_image) VALUES (?, ?, ?)",
                   (chat_id, user_prompt, result_image))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

# Usage example
# add_user_history_record('path_to_your_database.db', 'chat123', 'Hello, world!', image_data)
