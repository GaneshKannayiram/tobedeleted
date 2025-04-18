from sklearn.metrics.pairwise import cosine_similarity
from models import Job
import numpy as np

class Recommender:
    def __init__(self, feature_engineer):
        self.fe = feature_engineer
    
    def recommend(self, user_profile, jobs: list[Job], top_n=5):
        """Return top-N matching jobs"""
        user_vec = self.fe.transform_user(user_profile)
        job_vecs = np.array([self.fe.transform_job(job) for job in jobs])
        
        sim_scores = cosine_similarity(user_vec, job_vecs).flatten()
        ranked_indices = np.argsort(sim_scores)[::-1][:top_n]
        
        return [(jobs[i], sim_scores[i]) for i in ranked_indices]