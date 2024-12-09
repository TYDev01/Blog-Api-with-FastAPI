from pydantic import BaseModel, EmailStr
from datetime import datetime

class RegisterUser(BaseModel):
    email: EmailStr
    username: str
    password: str

    class Config:
        from_attributes = True


class RegisterResponse(BaseModel):
    id: int
    email: str
    username: str
    date_registered: datetime

    class Config:
        from_attributes = True


class PostSchema(BaseModel):
    title: str
    content: str
    category: str
    is_published: bool

    class Config:
        from_attributes = True

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    is_published: bool

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attribute = True