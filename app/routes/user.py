from fastapi import FastAPI, Depends, HTTPException, APIRouter, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from models.models import Registration
from schema.schema import RegisterUser, RegisterResponse, Token
from sqlmodel import Session, select
from utils.database import init_db, get_db
from utils.email import sendmail
from utils.utils import hashed_password
from utils.oauth2 import create_token

init_db()
app = FastAPI()
router = APIRouter()

@router.post("/register_user", status_code=status.HTTP_200_OK, response_model=RegisterResponse)
async def register_user(new_user: RegisterUser, db: Session = Depends(get_db)):
    # Check if email already exists
    email = new_user.email
    does_email_exists = db.exec(select(Registration).where(Registration.email == email)).first()
    if does_email_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with the email already exists.")

    # Check if username already exists
    username = new_user.username
    does_username_exists = db.exec(select(Registration).where(Registration.username == username)).first()

    if does_username_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Username already taken.")
    

    password = new_user.password
    if len(password) < 8:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="password should not be less than 8 characters.")
    hashing_the_password =  hashed_password(new_user.password)
    new_user.password = hashing_the_password

    store_data = Registration(**new_user.model_dump(exclude_none=True))
    db.add(store_data)
    db.commit()
    await sendmail(new_user.email, new_user.username)
    db.refresh(store_data)
    return store_data


@router.post("/login", response_model=Token)
async def login_user(users: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.exec(select(Registration).where(Registration.email == users.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid login details")
    
    does_password_match = hashed_password(user.password)

    if not does_password_match:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid login Details")
    
    access_token = create_token(data={"id": user.id})
    
    return {
        "token_type": "Bearer",
        "access_token": access_token
    }