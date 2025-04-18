# check_jobs.py
import sqlite3

conn = sqlite3.connect("backend/jobs.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM jobs;")
count = cursor.fetchone()[0]

print(f"Total jobs in DB: {count}")

conn.close()
