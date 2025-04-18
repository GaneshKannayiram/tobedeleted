"""

from data_fetcher import fetch_jobs_from_adzuna

jobs = fetch_jobs_from_adzuna(results_per_page=3)
print(f"Fetched {len(jobs)} jobs")
if jobs:
    print(f"First job: {jobs[0].title}")
    print(f"Skills: {jobs[0].skills}")

"""
import sqlite3

from database import Database

def test_connection():
    try:
        db = Database()
        print("✅ Connection successful!")
        print(f"Client: {db.supabase}")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
