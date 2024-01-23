FROM python:3.10.13-alpine

# Path: /app
WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install libpq-dev

COPY . .
RUN pip install psycopg2 requests python-telegram-bot python-dotenv
CMD ["python", "main.py"]
