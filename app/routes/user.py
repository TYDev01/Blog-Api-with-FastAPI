from fastapi import FastAPI, Depends, HTTPException
from models.models import Registeration
from sqlmodel import Session, select
from utils.database import init_db, get_db
init_db()
app = FastAPI()

@app.post("/register_user")
async def register_user(new_user: Registeration, db: Session = Depends(get_db)):
    try:
        email = new_user.email
        does_email_exists = db.exec(select(Registeration)).all()
        if does_email_exists:
            print(f"User with the email already exists.")
            raise HTTPException(status_code= 400, detail="User with the email already exists.")
        
        username = new_user.username
        does_username_exists = db.exec(select(Registeration)).all()

        if does_username_exists:
            print("Username already taken.")
            raise HTTPException(status_code=400, detail="Username already taken.")
    except:
        db.add(new_user)
