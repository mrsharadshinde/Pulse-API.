from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from app.schema.user_schema import UserResponse, UserOutWithPosts, CreateUser, UpdateUser
from app.Database.database import  get_db
from app.Database.user_model import Users
from app.Database.post_model import Posts
from app import utils
from datetime import datetime

#set prefix and tag for router
router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: CreateUser, db: Session = Depends(get_db) ):
    db_query = db.query(Users).filter(Users.email == user.email)
    db_user = db_query.first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    newUser = Users(**user.model_dump())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOutWithPosts)
def get_user(id: int, db: Session = Depends(get_db)):
    query = db.query(Users).filter(Users.id == id)
    user = query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    post_count = db.query(func.count(Posts.id)).filter(Posts.owner_id == user.id).scalar()
    return {"user": user, "post_count": post_count}

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
def get_all_users(
        db: Session = Depends(get_db),
        limit: int = 100,
        skip: int = 0,
        search: Optional[str] = "",
        sort: Optional[str] = "desc"
):
    query = db.query(Users).filter(Users.name.like(f"%{search}%"))

    if sort.lower() == "asc":
        query = query.order_by(Users.name.asc())
    else:
        query = query.order_by(Users.name.desc())

    users = query.limit(limit).offset(skip).all()
    return users

@router.patch("/{id}", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def update_user(id:int, userData: UpdateUser, db: Session = Depends(get_db)):
    db_query = db.query(Users).filter(Users.id == id)
    db_user = db_query.first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    hashed_password = utils.hash_password(userData.password)
    userData.password = hashed_password
    updated_user = userData.model_dump(exclude_unset=True)
    updated_user['updated_at'] = datetime.now()
    db_query.update(updated_user, synchronize_session=False)
    db.commit()
    return db_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int, db: Session = Depends(get_db)):
    db_query = db.query(Users).filter(Users.id == id)
    user = db_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found with id: {id}")
    db_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)