from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

from  app.logger import  logger
from app.utils import  limiter
from app.routers import posts, users, auth, vote

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs BEFORE the server starts
    logger.info("⚡ Pulse API Server is starting up...")
    yield

app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


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

# 2. Add a startup event to log when the server boots

@app.get("/")
def root():
    return {"message": "Welcome to pulse | All in one social app"}
