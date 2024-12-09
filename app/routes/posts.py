from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List
from utils.database import get_db
from schema.schema import PostSchema, PostResponse
from models.models import Posts


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(schema: PostSchema, db: Session = Depends(get_db)):
    new_posts = Posts(**schema.model_dump(exclude_none=True))
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts

# Get all posts
@router.get("/allposts", status_code=status.HTTP_200_OK, response_model=List[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    all_posts = db.exec(select(Posts)).all()
    if not all_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found.")
    
    return all_posts

# Get post by category
@router.get("/category/{category}", status_code=status.HTTP_200_OK, response_model=List[PostResponse])
def get_post_by_category(category: str, db: Session = Depends(get_db)):
    available_options = { "life_hack", "politics", "tech"}
    if category not in available_options:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post under the category '{category}' ")
    post = db.exec(select(Posts).where(Posts.category == category)).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post under the category '{category}'")
    
    return post

# Get post by iD
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def get_post_by_iD(id: int, db: Session = Depends(get_db)):
    post = db.exec(select(Posts).where(Posts.id == id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id '{id}' not found")
    
    return post
