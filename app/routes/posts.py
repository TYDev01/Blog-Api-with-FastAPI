from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List
from utils.database import get_db
from utils.oauth2 import get_current_user
from schema.schema import PostSchema, PostResponse, UpdateResponse, UpdateSchema
from models.models import Posts, Registration
from typing import Optional


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(schema: PostSchema, db: Session = Depends(get_db), user_auth: int = Depends(get_current_user)):
    print(user_auth)
    post_owner_id = user_auth
    compare_id = db.exec(select(Registration).where(Registration.id == post_owner_id)).first()
    if not compare_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    username = compare_id.username
    # get_author = check_author.username
    # author = get_author
    new_posts = Posts(**schema.model_dump(exclude_none=True), author=username)
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts

# Get all posts
@router.get("/allposts", status_code=status.HTTP_200_OK, response_model=List[PostResponse])
def get_all_posts(limit: int = 10, skip: int = 0, db: Session = Depends(get_db), user_auth: int = Depends(get_current_user), search: Optional[str] = ""):
    all_posts = db.exec(select(Posts).filter(Posts.title.ilike(search)).limit(limit).offset(skip)).all()
    if not all_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found.")
    
    return all_posts

# Get post by category
@router.get("/category/{category}", status_code=status.HTTP_200_OK, response_model=List[PostResponse])
def get_post_by_category(category: str, db: Session = Depends(get_db), user_auth: int = Depends(get_current_user)):
    available_options = { "life_hack", "politics", "tech"}
    if category not in available_options:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post under the category '{category}' ")
    post = db.exec(select(Posts).where(Posts.category == category)).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post under the category '{category}'")
    
    return post

# Get post by iD
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def get_post_by_iD(id: int, db: Session = Depends(get_db), user_auth: int = Depends(get_current_user)):
    post = db.exec(select(Posts).where(Posts.id == id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id '{id}' not found")
    
    return post

# Delete Post
@router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db), user_auth: int = Depends(get_current_user)):
    # First off get the post author
    # Secondly get the users username since we're using the username as author
    # - How do you get the username?
    # Thirdly, check if the post author is the same with the username trying to delete it.
    
    post = db.exec(select(Posts).where(Posts.id == id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post does not exists")
    
    get_user_with_the_id = db.exec(select(Registration).where(Registration.id == user_auth)).first()
    
    if post.author != get_user_with_the_id.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user.")
        
    db.delete(post)
    db.commit() 

    return {
        "message": "Post deleted successfully"
    }
# Update posts
@router.put("/{id}", response_model=UpdateResponse)
def update_post(id: int, update_schema: UpdateSchema, db: Session = Depends(get_db), user_auth: int = Depends(get_current_user)):
    post = db.exec(select(Posts).where(Posts.id == id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not available")
    print(post.author)
    get_user_with_the_id = db.exec(select(Registration).where(Registration.id == user_auth)).first()
    print(get_user_with_the_id.username)
    if post.author != get_user_with_the_id.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user.")
    
    post.title = update_schema.title
    post.content = update_schema.content
    post.category = update_schema.category
    post.is_published = update_schema.is_published

    db.add(post)
    db.commit()
    db.refresh(post)

    return post