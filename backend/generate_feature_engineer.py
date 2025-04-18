import joblib
from database import Database
from feature_engineer import FeatureEngineer
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting feature engineer generation...")
        
        # Get jobs from database
        db = Database()
        jobs = db.get_jobs_from_db()
        
        if not jobs:
            logger.error("No jobs found in database")
            return False
            
        logger.info(f"Training on {len(jobs)} jobs...")
        
        # Train feature engineer
        fe = FeatureEngineer()
        fe.fit(jobs)
        
        # Save the model
        joblib.dump(fe, 'feature_engineer.pkl')
        logger.info("Feature engineer saved to feature_engineer.pkl")
        return True
        
    except Exception as e:
        logger.error(f"Failed to generate feature engineer: {e}")
        return False

if __name__ == "__main__":
    if not main():
        sys.exit(1)