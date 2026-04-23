from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.Database.database import get_db
from app.Database import post_model, vote_model, user_model
from app.schema import vote_schema
from app import oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: vote_schema.Vote, db: Session = Depends(get_db), current_user: user_model.Users = Depends(oauth2.get_current_user)):

    #check if post exits
    post = db.query(post_model.Posts).filter(post_model.Posts.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {vote.post_id} does not exist")

    vote_query = db.query(vote_model.Vote).filter(
        vote_model.Vote.post_id == vote.post_id,
        vote_model.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.dir== 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail=f"User {current_user.id} has already voted on post {vote.post_id}"
            )

        new_vote = vote_model.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "Successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}
