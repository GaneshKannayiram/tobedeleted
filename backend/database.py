import sqlite3
from typing import List, Optional
from models import Job
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = 'jobs.db'):
        """Initialize SQLite database connection"""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()
        logger.info("Database connection established")

    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    company TEXT,
                    location TEXT,
                    description TEXT,
                    skills TEXT,  -- Stored as JSON array
                    experience_required TEXT,
                    job_type TEXT,
                    salary TEXT,
                    source_url TEXT,
                    posted_on TIMESTAMP
                )
            ''')
            self.conn.commit()
            logger.info("Jobs table created/verified")
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")
            raise

    def save_jobs(self, jobs: List[Job]) -> bool:
        """Save multiple jobs to the database"""
        try:
            self.cursor.executemany('''
                INSERT OR REPLACE INTO jobs VALUES (
                    :job_id, :title, :company, :location, :description,
                    :skills, :experience_required, :job_type, :salary,
                    :source_url, :posted_on
                )
            ''', [{
                'job_id': job.job_id,
                'title': job.title,
                'company': job.company,
                'location': job.location,
                'description': job.description,
                'skills': json.dumps(job.skills),
                'experience_required': job.experience_required,
                'job_type': job.job_type,
                'salary': job.salary,
                'source_url': job.source_url,
                'posted_on': job.posted_on.isoformat() if job.posted_on else None
            } for job in jobs])
            self.conn.commit()
            logger.info(f"Successfully saved {len(jobs)} jobs")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error saving jobs: {e}")
            self.conn.rollback()
            return False

    def get_jobs_from_db(self) -> List[Job]:
        """Retrieve all jobs from the database"""
        try:
            self.cursor.execute('SELECT * FROM jobs')
            rows = self.cursor.fetchall()
            
            jobs = []
            for row in rows:
                jobs.append(Job(
                    job_id=row[0],
                    title=row[1],
                    company=row[2],
                    location=row[3],
                    description=row[4],
                    skills=json.loads(row[5]),
                    experience_required=row[6],
                    job_type=row[7],
                    salary=row[8],
                    source_url=row[9],
                    posted_on=datetime.fromisoformat(row[10]) if row[10] else None
                ))
            logger.info(f"Retrieved {len(jobs)} jobs from database")
            return jobs
        except sqlite3.Error as e:
            logger.error(f"Error fetching jobs: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding skills JSON: {e}")
            return []

    def __del__(self):
        """Clean up database connection"""
        try:
            self.conn.close()
            logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database: {e}")