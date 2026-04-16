from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.Database.database import get_db
from app.Database import  user_model
from app import utils, oauth2
from app.schema import user_schema

router = APIRouter(
    tags=["authentication"]
)

@router.post("/login", response_model=user_schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    #look for the user by email
    #Note : OAuth2PasswordRequestForm always store the user email in variable called username
    user = db.query(user_model.Users).filter(user_model.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect username or password")

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect username or password")

    #Eveything matches create the JWT
    #we embed the user id to token so we know exactly who is logged in
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # Return the acces token to frontend
    return {"access_token": access_token, "token_type": "bearer"}

