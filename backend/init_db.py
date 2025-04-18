from database import Database
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_database():
    """Initialize the SQLite database"""
    try:
        db = Database()
        
        # Verify table exists and is accessible
        jobs = db.get_jobs_from_db()
        logger.info(f"Database initialized with {len(jobs)} existing jobs")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    if not initialize_database():
        sys.exit(1)