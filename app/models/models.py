from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime,timezone
from pydantic import EmailStr
from enum import Enum

class PostCategory(str, Enum):
    tech = "Tech"
    life_hack = "Life Hack"
    politics = "Politics"

class Registeration(SQLModel, table=True):
    __tablename__ = "user"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, unique=True)
    username: str = Field(unique=True, index=True)
    password: str
    date_registered: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Posts(SQLModel, table=True):
    __tablename__ = "posts"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, index=True)
    content: str = Field(nullable=False, index=False)
    category: PostCategory
    is_published: bool
    date_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))