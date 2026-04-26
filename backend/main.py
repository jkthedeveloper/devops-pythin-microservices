
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
	
	