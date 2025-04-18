from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Job:
    job_id: str
    title: str
    company: str
    location: str
    description: str
    skills: List[str]
    experience_required: str
    job_type: str
    salary: str
    source_url: str
    posted_on: datetime

@dataclass
class UserProfile:
    user_id: str
    desired_role: str
    locations: List[str]
    skills: List[str]
    experience_level: str
    min_salary: int