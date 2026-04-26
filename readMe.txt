2. Nginx Config (nginx/default.conf)


server {
    listen 80;

    location / {
        proxy_pass http://frontend:5000;
    }

    location /api/ {
        proxy_pass http://backend:8000/;
    }
}

===============================================================================================
3. Frontend (Flask) frontend/app.py

from flask import Flask
import requests
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379)

@app.route('/')
def home():
    count = r.incr('hits')
    api_response = requests.get("http://backend:8000/data").json()
    return f"""
    <h1>Flask Frontend</h1>
    <p>Visits: {count}</p>
    <p>Backend Data: {api_response}</p>
    """
	
=========================================================================================================
frontend/requirements.txt

flask
requests
redis

frontend/Dockerfile

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]

============================================================================================================
4. Backend (FastAPI) backend/main.py

from fastapi import FastAPI
import psycopg2

app = FastAPI()

def get_data():
    conn = psycopg2.connect(
        host="db",
        database="mydb",
        user="admin",
        password="admin"
    )
    cur = conn.cursor()
    cur.execute("SELECT 'Hello from PostgreSQL'")
    result = cur.fetchone()
    conn.close()
    return result[0]

@app.get("/data")
def read_data():
    return {"message": get_data()}
	
	
backend/requirements.txt

fastapi
uvicorn
psycopg2-binary

backend/Dockerfile

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]