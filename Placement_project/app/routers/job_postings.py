# app/routers/job_postings.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, scraper
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/job_postings/", response_model=schemas.JobPosting)
def create_job_posting(job_posting: schemas.JobPostingCreate, db: Session = Depends(get_db)):
    return crud.create_job_posting(db=db, job_posting=job_posting)

@router.get("/job_postings/", response_model=List[schemas.JobPosting])
def read_job_postings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    job_postings = crud.get_job_postings(db, skip=skip, limit=limit)
    return job_postings

@router.post("/scrape_jobs/")
def scrape_jobs():
    try:
        scraper.scrape_and_store_jobs()
        return {"status": "success", "message": "Job scraping triggered successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
