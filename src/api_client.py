# api_client.py

import json
import re
import requests
import ftfy

API_URL = "https://remoteok.com/api"


# ---------- Hjälpfunktioner ----------

def clean_html(text):
    """Tar bort HTML-taggar och onödiga whitespace."""
    if not isinstance(text, str):
        return ""
    text = ftfy.fix_text(text)               # fixar texten med ftfy
    text = re.sub(r"<[^>]+>", " ", text)     # ta bort taggar
    text = text.replace("&amp;", "&")
    text = text.replace("&nbsp;", " ")
    text = text.replace("&quot;", '"')
    text = text.replace("&#39;", "'")
    text = re.sub(r"\s+", " ", text)         # kollapsa whitespace
    return text.strip()


def is_ai_job(job, keywords):
    """Returnerar True om jobbet matchar något av nyckelorden (hela ord)."""
    title = job.get("position", "").lower()
    tags = " ".join(job.get("tags", [])).lower()
    text = title + " " + tags

    for word in keywords:
        pattern = r"\b" + re.escape(word.lower()) + r"\b"
        if re.search(pattern, text):
            return True
    return False


# ---------- API-hämtning ----------

def fetch_jobs(limit=5):
    """Hämtar jobb från RemoteOK API. Returnerar en lista av dicts."""
    headers = {
        "User-Agent": "ai-job-analyzer/1.0 (student project)"
    }

    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        response.raise_for_status()

        # Tolka råbytes som UTF-8
        text = response.content.decode("utf-8", errors="replace")

        data = json.loads(text)
        jobs = data[1:limit + 1]

        # Rensa HTML från description
        for job in jobs:
            if "description" in job:
                job["description"] = clean_html(job["description"])

        return jobs

    except requests.exceptions.Timeout:
        print("API-anropet tog för lång tid (timeout).")
        return []

    except requests.exceptions.HTTPError as e:
        print(f"HTTP-fel: {e}")
        return []

    except requests.exceptions.RequestException as e:
        print(f"Nätverksfel: {e}")
        return []


def fetch_ai_jobs(limit=5, keywords=None):
    """Hämtar AI-relaterade jobb från RemoteOK."""
    if keywords is None:
        keywords = [
            "AI", "artificial intelligence", "machine learning",
            "deep learning", "neural network", "NLP",
            "natural language processing", "computer vision",
            "reinforcement learning", "data scientist", "data engineer",
            "ML engineer", "MLOps"
        ]

    all_jobs = fetch_jobs(limit=50)
    ai_jobs = []

    for job in all_jobs:
        if is_ai_job(job, keywords):
            ai_jobs.append(job)
            if len(ai_jobs) >= limit:
                break

    return ai_jobs
