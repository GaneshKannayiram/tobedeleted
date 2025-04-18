from data_fetcher import fetch_jobs_from_adzuna
from database import Database
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update_jobs.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def update_jobs():
    """Fetch and save jobs from Adzuna to SQLite"""
    try:
        logger.info("Starting job update process...")
        
        # 1. Fetch jobs from Adzuna
        jobs = fetch_jobs_from_adzuna(results_per_page=10)
        logger.info(f"Fetched {len(jobs)} jobs from Adzuna API")
        
        if not jobs:
            logger.warning("No jobs received from Adzuna API")
            return False
            
        # 2. Save to SQLite
        db = Database()
        if db.save_jobs(jobs):
            logger.info(f"Successfully saved {len(jobs)} jobs to database")
            return True
        else:
            logger.error("Failed to save jobs to database")
            return False
            
    except Exception as e:
        logger.error(f"Job update failed: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    if update_jobs():
        sys.exit(0)
    else:
        sys.exit(1)