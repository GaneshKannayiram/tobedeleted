from update_jobs import update_jobs
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting initial database population...")
    if update_jobs():
        logger.info("Database populated successfully")
        sys.exit(0)
    else:
        logger.error("Failed to populate database")
        sys.exit(1)