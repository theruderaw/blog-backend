import jwt
from fastapi import FastAPI, HTTPException, status, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor, Json

from app.routes.articles import articles
from app.routes.utils import utils
from app.routes.messages import messages

FRONTEND_URL = "https://blog-frontend-swart-one.vercel.app/"

app = FastAPI(title="Blog Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[FRONTEND_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articles.router)
app.include_router(utils.router)
app.include_router(messages.router)
