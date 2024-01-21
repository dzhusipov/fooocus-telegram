FROM python:3.10.13-alpine

# Path: /app
WORKDIR /app

# Path: /app/requirements.txt
COPY . .

# Path: /app
RUN pip install requests python-telegram-bot python-dotenv


# Path: /app
COPY . .

# Path: /app
CMD ["python", "main.py"]
