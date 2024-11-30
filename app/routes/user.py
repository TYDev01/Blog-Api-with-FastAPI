from fastapi import FastAPI, Depends, HTTPException, APIRouter, status
from models.models import Registeration
from sqlmodel import Session, select
from utils.database import init_db, get_db
import bcrypt
init_db()
app = FastAPI()
router = APIRouter()

@router.post("/register_user", status_code=status.HTTP_200_OK)
async def register_user(new_user: Registeration, db: Session = Depends(get_db)):
    email = new_user.email
    does_email_exists = db.exec(select(Registeration).where(Registeration.email == email)).first()
    if does_email_exists:
        print(f"User with the email already exists.")
        raise HTTPException(status_code= 400, detail="User with the email already exists.")
    else:
        print("Email is available")

    username = new_user.username
    does_username_exists = db.exec(select(Registeration).where(Registeration.username == username)).first()

    if does_username_exists:
        print("Username already taken.")
        raise HTTPException(status_code=400, detail="Username already taken.")
    else:
        print("Username is available")
    password = new_user.password
    hashing_the_password =  bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_user.password = hashing_the_password
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return {
        "response": "Registration successfull."
    }
