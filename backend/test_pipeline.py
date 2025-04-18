from data_fetcher import fetch_jobs_from_adzuna
from database import Database

def test_full_pipeline():
    print("Testing Adzuna to Supabase pipeline...")
    
    # Step 1: Fetch jobs
    jobs = fetch_jobs_from_adzuna(results_per_page=3)
    print(f"Fetched {len(jobs)} jobs from Adzuna")
    
    # Step 2: Initialize DB
    db = Database()
    
    # Step 3: Save jobs
    db.save_jobs(jobs)
    print("Jobs saved to Supabase")
    
    # Step 4: Verify
    saved_jobs = db.supabase.table("jobs").select("*").execute()
    print(f"Found {len(saved_jobs.data)} jobs in database")

if __name__ == "__main__":
    test_full_pipeline()