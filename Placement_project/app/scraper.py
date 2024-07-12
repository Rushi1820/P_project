# app/scraper.py

import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from apscheduler.schedulers.blocking import BlockingScheduler
from app import crud, schemas
from app.database import SessionLocal

def read_company_details(file_path):
    df = pd.read_excel(file_path)
    return df.to_dict(orient='records')

def scrape_job_postings(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # This part will vary depending on the structure of the job listing page
    job_postings = []
    for job_card in soup.select('selector_for_job_card'):
        job_title = job_card.select_one('selector_for_job_title').text.strip()
        location = job_card.select_one('selector_for_location').text.strip()
        deadline = job_card.select_one('selector_for_deadline').text.strip()
        description = job_card.select_one('selector_for_description').text.strip()
        
        job_postings.append({
            'title': job_title,
            'location': location,
            'deadline': deadline,
            'description': description
        })
    
    return job_postings

def scrape_and_store_jobs():
    db: Session = SessionLocal()
    file_path = os.path.join(os.path.dirname(__file__), '../data/companieslinks-list.xlsx')
    companies = read_company_details(file_path)
    
    for company in companies:
        job_postings = scrape_job_postings(company['CareerLink'])
        for job in job_postings:
            if 'fresher' in job['description'].lower() or '0-1 years' in job['description'].lower():
                job_data = schemas.JobPostingCreate(
                    title=job['title'],
                    location=job['location'],
                    deadline=job['deadline'],
                    description=job['description'],
                    company=company['CompnayName']
                )
                crud.create_job_posting(db, job_data)
    
    db.close()

scheduler = BlockingScheduler()
scheduler.add_job(scrape_and_store_jobs, 'cron', hour=10)
scheduler.start()
