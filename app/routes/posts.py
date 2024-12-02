from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from utils.database import get_db
from schema.schema import PostSchema, PostResponse
from models.models import Posts


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(schema: PostSchema, db: Session = Depends(get_db)):
    new_posts = Posts(**schema.model_dump())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def get_post_by_iD(id: int, db: Session = Depends(get_db)):
    post = db.exec(select(Posts).where(Posts.id == id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_200_OK, detail=f"Post with the id '{id}' not found")
    
    return post