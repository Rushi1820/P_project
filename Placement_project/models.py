# app/models.py

from sqlalchemy import Column, Integer, String, Text
from database import Base

class JobPosting(Base):
    __tablename__ = 'job_postings'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    location = Column(String, index=True)
    deadline = Column(String)
    description = Column(Text)
    company = Column(String, index=True)
