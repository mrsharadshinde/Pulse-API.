from passlib.context import CryptContext
from slowapi import Limiter
from slowapi.util import  get_remote_address

pwd_context =   CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

limiter = Limiter(key_func=get_remote_address)