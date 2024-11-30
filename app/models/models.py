from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Registeration(SQLModel, table=True):
    __tablename__ = "user"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    username: str = Field(unique=True, index=True)
    password: str