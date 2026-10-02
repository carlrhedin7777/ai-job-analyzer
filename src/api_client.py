# api_client.py

import json  # importerar json-biblioteket för att hantera JSON-data
import re  # importerar re-biblioteket för att hantera reguljära uttryck
import requests  # importerar requests-biblioteket för att göra HTTP-anrop


# URL till RemoteOK API som vi ska hämta jobbannonser från
api_url = "https://remoteok.com/api"


# Hämtar jobbannonser från API. Ta emot en parameter limit som anger hur många annonser som ska hämtas (standard är 5).

def fetch_jobs(limit=5):

    headers = {
        # Anger en User-Agent för att undvika blockering
        "User-Agent": "ai-job-analyzer/1.0"
    }

   # Hämtar jobbannonser från RemoteOK API.
   # Returnerar en lista med jobbannonser (dicts).

    try:
        # Timeout på 10 sekunder om servern inte svarar
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()

       # Tolka rådata som utf-8 och ladda den som JSON
        text = response.content.decode("utf-8")
        data = json.loads(text)

        # Hoppar över den första posten som är metadata och tar de första limit annonserna
        jobs = data[1:limit + 1]
        return jobs

    except requests.exceptions.timeout:
        print("API-anropet tog för lång tid (timeout).")
        return []

    except requests.exceptions.RequestException as e:
        print(f"Nätverksfel: {e}")
        return []

    except requests.exceptions.HTTPError as e:
        print(f"HTTP-fel: {e}")
        return []


def is_ai_job(job, keywords):

    # returnerar True om någon av nyckelorden finns i jobbannonsens titel eller taggar, annars False
    # Hämtar jobbannonsens titel och konverterar den till små bokstäver
    title = job.get("position", "").lower()
    # Hämtar jobbannonsens taggar och konverterar dem till små bokstäver
    tags = " ".join(job.get("tags", [])).lower()
    text = title + " " + tags  # Skapar en sträng som innehåller både titel och taggar

    for word in keywords:  # Loopar igenom varje nyckelord i listan keywords
        # Skapar ett regex-mönster för att matcha hela ord
        pattern = r"\b" + re.escape(word.lower()) + r"\b"
        if re.search(pattern, text):  # Om nyckelordet finns i texten (titel + taggar), returnera True
            return True
    return False  # Om inget nyckelord matchar, returnera False


def fetch_ai_jobs(limit=5, keywords=None):
    # Hämtar jobbannonser och filtrerar ut de som är AI-relaterade baserat på nyckelord.
    if keywords is None:
        keywords = [
            "AI", "artificial intelligence", "machine learning",
            "deep learning", "neural network", "NLP", "natural language processing",
            "computer vision", "reinforcement learning"
        ]

    all_jobs = fetch_jobs(limit=50)  # Hämtar jobbannonser
    ai_jobs = []

    for job in all_jobs:  # Loopar igenom alla jobbannonser
        if is_ai_job(job, keywords):  # Om jobbet är AI-relaterat
            ai_jobs.append(job)  # Lägg till det i listan ai_jobs
            if len(ai_jobs) >= limit:  # Om vi har nått gränsen för hur många annonser vi vill ha
                break  # Avsluta loopen

    return ai_jobs  # Returnerar listan med AI-relaterade jobbannonser
