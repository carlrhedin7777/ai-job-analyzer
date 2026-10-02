# api_client.py

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
        response.encoding = 'utf-8'  # Säkerställer att vi tolkar svaret som UTF-8
        response.raise_for_status()  # Kastar ett undantag om statuskoden inte är 200
        data = response.json()

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
