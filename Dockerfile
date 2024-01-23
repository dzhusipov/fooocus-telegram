FROM python:3.10.13-alpine

# Path: /app
WORKDIR /app

RUN apk update
RUN apk add libpq-dev
RUN apk add gcc

COPY . .
RUN pip install psycopg2-binary requests python-telegram-bot python-dotenv
CMD ["python", "main.py"]
