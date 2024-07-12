# app/main.py

from fastapi import FastAPI
from app.models import Base
from app.database import engine
from app.routers import job_postings
import uvicorn


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(job_postings.router, prefix="/api/v1", tags=["job_postings"])

