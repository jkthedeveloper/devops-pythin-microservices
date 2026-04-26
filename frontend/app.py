
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