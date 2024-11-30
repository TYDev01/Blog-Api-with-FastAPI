from fastapi import FastAPI
from utils.database import init_db
from routes.user import router as user_router
app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["Users"])

init_db()

@app.get("/")
def home_view():
    return {"response": "Welcome to Our Blog"}

