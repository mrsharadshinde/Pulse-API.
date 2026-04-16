from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Swap out the hardcoded string for the dynamic settings
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


# create the engine (actual connection)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#create session factor for our routes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# the base class for our models
Base = declarative_base()


#dependacy : Opens db session for request then safly close it
def get_db():
    db = SessionLocal()
    try: yield db
    finally:
        db.close()
