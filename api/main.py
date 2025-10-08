from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "todos_db")
DB_USER = os.getenv("DB_USER", "todo_user")
DB_PASS = os.getenv("DB_PASS", "todo_pass")

def get_conn():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST
    )

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/todos/{task}")
def create_task(task: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
    conn.commit()
    cur.close()
    conn.close()
    return {"task": task, "status": "created"}

@app.get("/api/todos")
def list_tasks():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, task, done FROM todos")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"todos": rows}
