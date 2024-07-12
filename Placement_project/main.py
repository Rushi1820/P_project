from fastapi import FastAPI
from models import Base
from database import engine
from routers import job_postings
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(job_postings.router, prefix="/api/v1", tags=["job_postings"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug")

