from fastapi import FastAPI, Depends, HTTPException, APIRouter, status
from models.models import Registeration
from schema.schema import RegisterUser
from sqlmodel import Session, select
from utils.database import init_db, get_db
from utils.email import sendmail
import bcrypt

init_db()
app = FastAPI()
router = APIRouter()

@router.post("/register_user", status_code=status.HTTP_200_OK)
async def register_user(new_user: RegisterUser, db: Session = Depends(get_db)):
    # Check if email already exists
    email = new_user.email
    does_email_exists = db.exec(select(Registeration).where(Registeration.email == email)).first()
    if does_email_exists:
        print(f"User with the email already exists.")
        raise HTTPException(status_code= 400, detail="User with the email already exists.")
    else:
        print("Email is available")

    # Check if username already exists
    username = new_user.username
    does_username_exists = db.exec(select(Registeration).where(Registeration.username == username)).first()

    if does_username_exists:
        print("Username already taken.")
        raise HTTPException(status_code=400, detail="Username already taken.")
    else:
        print("Username is available")
    

    password = new_user.password
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="password should not be less than 8 characters.")
    hashing_the_password =  bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    store_data = Registeration(
        email=new_user.email,
        username=new_user.username,
        password=hashing_the_password,
        
    )
    db.add(store_data)
    db.commit()
    await sendmail(new_user.email, new_user.username)
    db.refresh(store_data)
    print(store_data)
    return {
        "response": "Registration successfull."
    }


@router.post("/login")
async def login_user(users: Registeration, db: Session = Depends(get_db)):
    user = db.exec(select(Registeration).where(Registeration.username == users.username)).first()
    if not user:
        raise HTTPException(status_code=400, detail="username not found")
    
    does_password_match = bcrypt.checkpw(users.password.encode("utf-8"), user.password.encode("utf-8"))

    if not does_password_match:
        raise HTTPException(status_code=400, detail="password does not match")
    
    return {
        "response": "login successful."
    }