from fastapi import FastAPI
app = FastAPI()
from utils.database import init_db

init_db()

@app.get("/")
def home_view():
    return {"response": "Welcome to Our Blog"}

