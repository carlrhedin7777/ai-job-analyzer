
from api_client import fetch_jobs

jobs = fetch_jobs(limit=3)
print(f"Hämtade {len(jobs)} jobb från API.")
for job in jobs:
    print(f"- {job.get('position', '?')} hos {job.get('company', '?')}")


# test_api.py
