import requests
import os
from models import Job
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def fetch_jobs_from_adzuna(country='in', results_per_page=5) -> list[Job]:
    """Fetch jobs from Adzuna API (corrected endpoint)"""
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    base_url = "https://api.adzuna.com/v1/api/jobs"
    
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'results_per_page': results_per_page,
        'content-type': 'application/json'
    }
    
    try:
        # Correct endpoint format for Adzuna
        response = requests.get(f"{base_url}/{country}/search/1", params=params)
        response.raise_for_status()
        jobs_data = response.json().get("results", [])
        
        return [
            Job(
                job_id=str(job["id"]),
                title=job["title"],
                company=job.get("company", {}).get("display_name", "N/A"),
                location=job["location"]["display_name"],
                description=job["description"],
                skills=extract_skills(job["description"]) if job.get("description") else [],
                experience_required=job.get("contract_type", ""),
                job_type=job.get("contract_time", ""),
                salary=f"{job.get('salary_min', 'N/A')}-{job.get('salary_max', 'N/A')} {job.get('salary_currency', '')}",
                source_url=job["redirect_url"],
                posted_on=datetime.strptime(job["created"], "%Y-%m-%dT%H:%M:%SZ") if "created" in job else None
            )
            for job in jobs_data
        ]
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching jobs from Adzuna: {e}")
        return []

def extract_skills(description):
    """Helper to extract skills from description"""
    skills_list = ["python", "django", "sql", "aws", "flask", "machine learning"]
    return [skill for skill in skills_list if skill in description.lower()]