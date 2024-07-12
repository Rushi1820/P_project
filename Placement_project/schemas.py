# app/schemas.py

from pydantic import BaseModel, Field

class JobPostingBase(BaseModel):
    title: str
    location: str
    deadline: str
    description: str
    company: str

class JobPostingCreate(JobPostingBase):
    pass

class JobPosting(JobPostingBase):
    id: int = Field(..., alias='id')

    class Config:
        from_attributes = True
