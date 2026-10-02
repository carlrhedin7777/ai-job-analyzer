
# test_api.py

from api_client import fetch_ai_jobs

jobs = fetch_ai_jobs(limit=5)
print(f"Hämtade {len(jobs)} AI-relaterade jobb från API.")
for job in jobs:
    print(f"- {job.get('position', '?')} hos {job.get('company', '?')}")
