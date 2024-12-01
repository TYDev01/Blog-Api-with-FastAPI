from fastapi import FastAPI
from utils.database import init_db
from routes.user import router as user_router
from routes.posts import router as post_router
app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(post_router, prefix="/post", tags=["Post"])

init_db()

@app.get("/")
def home_view():
    return {"response": "Welcome to Our Blog"}

