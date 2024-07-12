# app/crud.py

from sqlalchemy.orm import Session
from models import JobPosting
from schemas import JobPostingCreate

def create_job_posting(db: Session, job_posting: JobPostingCreate):
    db_job_posting = JobPosting(
        title=job_posting.title,
        location=job_posting.location,
        deadline=job_posting.deadline,
        description=job_posting.description,
        company=job_posting.company
    )
    db.add(db_job_posting)
    db.commit()
    db.refresh(db_job_posting)
    return db_job_posting

def get_job_postings(db: Session, skip: int = 0, limit: int = 10):
    return db.query(JobPosting).offset(skip).limit(limit).all()
