import jwt
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime, timedelta, timezone
from schema.schema import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_schem = OAuth2PasswordBearer(tokenUrl='login')



SECRET_KEY = os.getenv("SECRETY_KEY")
ALGORITHM = os.getenv("ALGORITHM")
expires = int(os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES"))

# To create an access token
def create_token(data: dict):
    to_encode = data.copy()
    expiring_time = datetime.now(timezone.utc) + timedelta(minutes=expires)
    to_encode.update({"exp": expiring_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# To verify the access token:
def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")

        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    return token_data
    

def get_current_user(token: str = Depends(oauth2_schem)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not Validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"},)
    return verify_token(token, credentials_exception)