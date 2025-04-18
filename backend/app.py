from flask import Flask, request, jsonify
from models import UserProfile
from recommender import Recommender
from feature_engineer import FeatureEngineer
import joblib
import redis
import logging
from typing import List
from database import Database
from models import Job

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
cache = redis.Redis(host='localhost', port=6379)

# Initialize components
try:
    fe = joblib.load('feature_engineer.pkl') 
    recommender = Recommender(fe)
    db = Database()
    logger.info("Application components initialized successfully")
except Exception as e:
    logger.critical(f"Failed to initialize application: {e}")
    raise

def get_jobs_from_db() -> List[Job]:
    """Wrapper function for job retrieval"""
    try:
        return db.get_jobs_from_db()
    except Exception as e:
        logger.error(f"Error fetching jobs from DB: {e}")
        return []

@app.route('/recommend', methods=['POST'])
def recommend():
    """Recommend jobs based on user profile"""
    try:
        data = request.json
        logger.info(f"Received recommendation request: {data}")
        
        user = UserProfile(**data)
        cache_key = f"recs:{user.user_id}"
        
        # Check cache
        cached = cache.get(cache_key)
        if cached:
            logger.debug(f"Returning cached results for user {user.user_id}")
            return jsonify({"jobs": cached})
        
        # Get and process jobs
        jobs = get_jobs_from_db()
        if not jobs:
            logger.warning("No jobs found in database")
            return jsonify({"error": "No jobs available"}), 503
            
        recommendations = recommender.recommend(user, jobs)
        cache.setex(cache_key, 3600, recommendations)
        
        logger.info(f"Generated {len(recommendations)} recommendations for user {user.user_id}")
        return jsonify({"jobs": recommendations})
        
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logger.critical(f"Flask application failed: {e}")