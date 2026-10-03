# api_client.py

import ftfy
import json
import re
import requests


API_URL = "https://remoteok.com/api"


def clean_text(text):
    """Tar bort HTML och fixar teckenkodning."""
    text = ftfy.fix_text(text)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def fetch_jobs(limit=5):
    """Hämtar AI-jobb från RemoteOK. Returnerar en lista av dicts."""
    headers = {"User-Agent": "ai-job-analyzer/1.0"}

    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = json.loads(response.content.decode("utf-8", errors="replace"))
    except requests.exceptions.RequestException as e:
        print(f"Nätverksfel: {e}")
        return []

    # Filtrera på AI-nyckelord i titeln
    keywords = ["ai", "machine learning", "ml", "deep learning", "nlp"]
    ai_jobs = []
    for job in data[1:]:
        title = job.get("position", "").lower()
        if any(re.search(r"\b" + re.escape(k) + r"\b", title) for k in keywords):
            ai_jobs.append(job)
        if len(ai_jobs) >= limit:
            break

    # Rensa HTML i beskrivningen
    for job in ai_jobs:
        job["description"] = clean_text(job.get("description", ""))

    return ai_jobs
