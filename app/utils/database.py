from fastapi import Depends, FastAPI, Query
from sqlmodel import Field, SQLModel, create_engine, Session
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine =create_engine(DATABASE_URL)

 # Dependency, it's responsible for  talking with the database. 
def init_db():
    try:
        SQLModel.metadata.create_all(engine)
        print("Database created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")


def get_db():
    with Session(engine) as session:
        yield session # Get a session anytime we talk to the database.
