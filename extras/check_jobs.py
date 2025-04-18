from db.db_utils import get_all_jobs_from_db

jobs = get_all_jobs_from_db()
print(f"Total jobs in DB: {len(jobs)}")
if jobs:
    print("Example job title:", jobs[0].get('title'))
