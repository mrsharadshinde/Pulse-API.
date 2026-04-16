from os.path import join

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app import oauth2
from sqlalchemy import func

# database session models and schemas
from app.Database.database import get_db
from app.Database import post_model, vote_model
from app.schema.post_schema import PostResponse,CreatePost, UpdatePost, PostOut

# create the router
# prefix = "/posts" every routes bellow automatically start with /posts
#tag=["post"] group these beautifully in your swagger UI

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)

#Create the new posts
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(
        post: CreatePost,
        db: Session = Depends(get_db),
        current_user:int =  Depends(oauth2.get_current_user)
):
    # unpack pydantic model to sqlalchemy mode
    new_post = post_model.Posts(owner_id= current_user.id ,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# get all posts
@router.get("/", response_model=List[PostOut])
def get_posts(
        db: Session = Depends(get_db),
        limit: int = 100,
        skip: int = 0,
        search: Optional[str] = "",
        sort: Optional[str] = "desc"
):

    query = db.query(post_model.Posts, func.count(vote_model.Vote.post_id).label("votes")) \
        .join(vote_model.Vote, vote_model.Vote.post_id == post_model.Posts.id, isouter=True) \
        .group_by(post_model.Posts.id) \
        .filter(post_model.Posts.title.contains(search))

    if sort.lower() == "asc":
        query = query.order_by(post_model.Posts.id.asc())
    else:
        query = query.order_by(post_model.Posts.id.desc())

    posts = query.limit(limit).offset(skip).all()
    return posts

#get the single posts
@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(post_model.Posts, func.count(vote_model.Vote.post_id).label("votes")) \
    .join(vote_model.Vote, vote_model.Vote.post_id == post_model.Posts.id, isouter=True) \
    .group_by(post_model.Posts.id) \
    .filter(post_model.Posts.id == post_id)\
    .first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return db_post

#Update post
@router.patch("/{post_id}", response_model=PostResponse)
def update_post(
        post_id: int,
        post_data: UpdatePost,
        db: Session = Depends(get_db),
        current_user:int =  Depends(oauth2.get_current_user)
):
    db_query = db.query(post_model.Posts).filter(post_model.Posts.id == post_id)
    db_post = db_query.first()
    if db_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found with id: {post_id}")

    # 2. THE OWNERSHIP CHECK!
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

    updated_data = post_data.model_dump(exclude_unset=True)
    updated_data["updated_at"] = datetime.now()
    db_query.update(updated_data, synchronize_session=False)
    db.commit()
    return db_query.first()

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        post_id: int, db: Session = Depends(get_db),
        current_user:int =  Depends(oauth2.get_current_user
        )):
    db_query = db.query(post_model.Posts).filter(post_model.Posts.id == post_id)
    db_post = db_query.first()
    if db_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found with id: {post_id}")
    # 2. THE OWNERSHIP CHECK!
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    db_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
