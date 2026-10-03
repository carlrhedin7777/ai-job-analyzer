# api_client.py


# api_client.py

import ftfy
import json
import re
import requests


API_URL = "https://remoteok.com/api"


def clean_html(text):
    """Tar bort HTML och fixar teckenkodning."""
    text = ftfy.fix_text(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_ai_job(job, keywords):
    """Returnerar True om titeln eller taggarna matchar ett AI-nyckelord."""
    text = (job.get("position", "") + " " +
            " ".join(job.get("tags", []))).lower()
    for word in keywords:
        if re.search(r"\b" + re.escape(word.lower()) + r"\b", text):
            return True
    return False


def fetch_jobs(limit=5, ai_only=False):
    """Hämtar jobb från RemoteOK. Om ai_only=True filtreras AI-jobb ut."""
    headers = {"User-Agent": "ai-job-analyzer/1.0"}

    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = json.loads(response.content.decode("utf-8", errors="replace"))
    except requests.exceptions.RequestException as e:
        print(f"Nätverksfel: {e}")
        return []

    jobs = data[1:]

    # Rensa HTML på varje beskrivning
    for job in jobs:
        if "description" in job:
            job["description"] = clean_html(job["description"])

    # Filtrera på AI om användaren vill
    if ai_only:
        keywords = ["AI", "machine learning", "deep learning",
                    "neural network", "NLP", "computer vision", "ML engineer"]
        jobs = [j for j in jobs if is_ai_job(j, keywords)]

    return jobs[:limit]
