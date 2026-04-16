from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers import posts, users, auth, vote
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

app.include_router(vote.router)
@app.get("/")
def root():
    return {"message": "welcome to my api"}
