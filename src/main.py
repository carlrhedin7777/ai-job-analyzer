# main.py är huvudfilen som kör programmet. Den innehåller menyval och flödet för att analysera jobbannonser.

from api_client import fetch_ai_jobs
from models import JobAd, AIJob, JobAnalyzer, Candidate
import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(__file__))


DATA_FILE = "data/jobads.json"
OUTPUT_FILE = "output/results.json"

SKILLS_TO_FIND = [
    "Python", "SQL", "Git", "Docker", "AWS",
    "TensorFlow", "PyTorch", "Machine Learning", "NLP",
]


# ---------- Inläsning ----------

def load_job_ads(filepath):
    """Läser jobbannonser från en JSON-fil. Returnerar en lista av dicts."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Filen hittades inte: {filepath}")
        return []
    except json.JSONDecodeError:
        print(f"Filen är inte giltig JSON: {filepath}")
        return []


def build_job_objects(raw_ads):
    """Omvandlar dicts från JSON/API till JobAd-objekt."""
    jobs = []
    for ad in raw_ads:
        # JSON-filen använder 'id', API:et använder 'id' och 'position'
        ad_id = ad.get("id", 0)
        title = ad.get("title") or ad.get("position", "Okänd titel")
        company = ad.get("company", "Okänt företag")
        location = ad.get("location", "Okänd plats")
        description = ad.get("description", "")
        jobs.append(JobAd(ad_id, title, company, location, description))
    return jobs


# ---------- Analys ----------

def analyze_jobs(jobs, analyzer):
    """Analyserar en lista av JobAd-objekt. Returnerar en lista av resultat-dicts."""
    results = []
    for job in jobs:
        found = analyzer.analyze(job)
        results.append({
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "skills": found,
            "skill_count": len(found),
        })
    return results


# ---------- Sparande ----------

def save_results(results, filepath):
    """Sparar analysresultat till en JSON-fil."""
    try:
        # Se till att mappen finns
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        payload = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "count": len(results),
            "results": results,
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        print(f"Resultat sparat till {filepath}")
    except OSError as e:
        print(f"Kunde inte spara filen: {e}")


# ---------- Meny & flöde ----------

def show_menu():
    print()
    print("=== AI Job Analyzer ===")
    print("1. Analysera lokala jobbannonser (JSON)")
    print("2. Hämta och analysera AI-jobb från API")
    print("3. Matcha dina kompetenser mot annonser")
    print("4. Avsluta")
    print()


def run_local_analysis(analyzer):
    print("\nLäser lokala annonser...")
    raw_ads = load_job_ads(DATA_FILE)
    if not raw_ads:
        print("Inga annonser att analysera.")
        return

    jobs = build_job_objects(raw_ads)
    results = analyze_jobs(jobs, analyzer)

    for r in results:
        print(
            f"- {r['title']} hos {r['company']} ({r['skill_count']} kompetenser)")

    save_results(results, OUTPUT_FILE)


def run_api_analysis(analyzer):
    print("\nHämtar jobb från API...")
    raw_jobs = fetch_ai_jobs(limit=5)
    if not raw_jobs:
        print("Inga jobb hämtades.")
        return

    jobs = build_job_objects(raw_jobs)
    results = analyze_jobs(jobs, analyzer)

    for r in results:
        print(
            f"- {r['title']} hos {r['company']} ({r['skill_count']} kompetenser)")

    save_results(results, OUTPUT_FILE)


def ask_for_skills():
    """Frågar användaren efter kompetenser. Returnerar en lista."""
    text = input("Ange dina kompetenser (kommaseparerade): ").strip()
    if not text:
        return []
    return [s.strip() for s in text.split(",") if s.strip()]


def run_match_analysis(analyzer):
    """Matchar användarens kompetenser mot en vald annons."""
    print("\nVar vill du matcha mot?")
    print("1. Lokala annonser (JSON)")
    print("2. API-jobb")
    source = input("Välj (1-2): ").strip()

    if source == "1":
        raw_ads = load_job_ads(DATA_FILE)
    elif source == "2":
        raw_ads = fetch_ai_jobs(limit=5)
    else:
        print("Ogiltigt val.")
        return

    if not raw_ads:
        print("Ingen data att matcha mot.")
        return

    jobs = build_job_objects(raw_ads)
    skills = ask_for_skills()
    if not skills:
        print("Inga kompetenser angivna.")
        return

    candidate = Candidate("Du", skills)
    print(f"\nMatchar {candidate} mot {len(jobs)} annonser:\n")

    for job in jobs:
        result = analyzer.match(job, candidate)
        print(f"--- {job} ---")
        print(f"  Matchningsprocent: {result['percent']}%")
        print(f"  Matchande: {', '.join(result['matching']) or '–'}")
        print(f"  Saknade:   {', '.join(result['missing']) or '–'}")
        print()


def main():
    analyzer = JobAnalyzer(SKILLS_TO_FIND)

    while True:
        show_menu()
        choice = input("Välj ett alternativ (1-4): ").strip()

        if choice == "1":
            run_local_analysis(analyzer)
        elif choice == "2":
            run_api_analysis(analyzer)
        elif choice == "3":
            run_match_analysis(analyzer)
        elif choice == "4":
            print("Hej då!")
            break
        else:
            print("Ogiltigt val, försök igen.")


if __name__ == "__main__":
    main()
