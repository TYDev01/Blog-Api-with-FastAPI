from pydantic import BaseModel
from datetime import datetime

class RegisterUser(BaseModel):
    email: str
    username: str
    password: str

    class Config:
        from_attributes = True