FROM python:3.10.13-alpine

# Path: /app
WORKDIR /app

# Path: /app/requirements.txt
COPY requirements.txt .

# Path: /app
RUN pip install -r requirements.txt

# Path: /app
COPY . .

# Path: /app
CMD ["python", "main.py"]
