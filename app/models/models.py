from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime,timezone
from pydantic import EmailStr

class Registeration(SQLModel, table=True):
    __tablename__ = "user"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, unique=True)
    username: str = Field(unique=True, index=True)
    password: str
    date_registered: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

