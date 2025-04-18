from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import logging
from typing import List
from models import Job

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FeatureEngineer:
    def __init__(self):
        """Initialize feature engineering components"""
        self.tfidf = TfidfVectorizer(
            stop_words='english',
            min_df=2,  # Minimum document frequency
            max_features=10000  # Limit vocabulary size
        )
        self.skill_encoder = MultiLabelBinarizer()
        logger.info("Feature engineering components initialized")

    def fit(self, jobs: List[Job]):
        """Train feature encoders with validation"""
        try:
            if not jobs:
                raise ValueError("Empty jobs list provided")
                
            # Prepare text data
            texts = [f"{job.title} {job.description}" for job in jobs]
            if not any(text.strip() for text in texts):
                raise ValueError("All job texts are empty")
            
            # Fit transformers
            self.tfidf.fit(texts)
            self.skill_encoder.fit([job.skills for job in jobs])
            
            logger.info(f"Successfully trained on {len(jobs)} jobs")
            logger.debug(f"Vocabulary size: {len(self.tfidf.vocabulary_)}")
            logger.debug(f"Skill categories: {len(self.skill_encoder.classes_)}")
            
        except Exception as e:
            logger.error(f"Error during fitting: {e}")
            raise

    def transform_job(self, job: Job) -> np.ndarray:
        """Convert Job to feature vector with error handling"""
        try:
            text = f"{job.title} {job.description}"
            title_vec = self.tfidf.transform([text])
            skills_vec = self.skill_encoder.transform([job.skills])
            return np.hstack([title_vec.toarray(), skills_vec])
        except Exception as e:
            logger.error(f"Error transforming job {job.job_id}: {e}")
            raise

    def transform_user(self, user_profile) -> np.ndarray:
        """Convert UserProfile to feature vector"""
        try:
            # Create a dummy job from user profile
            dummy_job = Job(
                job_id="user_profile",
                title=user_profile.desired_role,
                company="",
                location="",
                description="",
                skills=user_profile.skills,
                experience_required=user_profile.experience_level,
                job_type="",
                salary="",
                source_url="",
                posted_on=None
            )
            return self.transform_job(dummy_job)
        except Exception as e:
            logger.error(f"Error transforming user profile: {e}")
            raise