# main.py

from models import JobAd, AIJob, JobAnalyzer
from api_client import fetch_jobs
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))


DATA_FILE = "data/jobads.json"
SKILLS = ["Python", "SQL", "Git", "Docker", "AWS",
          "TensorFlow", "PyTorch", "Machine Learning", "NLP"]


def load_local_jobs():
    """Läser lokala annonser från JSON. Returnerar en lista av JobAd."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [JobAd(ad["title"], ad["description"]) for ad in raw]
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Kunde inte läsa {DATA_FILE}: {e}")
        return []


def load_api_jobs():
    """Hämtar AI-jobb från API. Returnerar en lista av AIJob."""
    raw = fetch_jobs(limit=5)
    return [AIJob(j["position"], j.get("description", ""), "AI") for j in raw]


def analyze_and_match(jobs, analyzer):
    """Analyserar jobben och frågar sedan om användaren vill matcha."""
    for job in jobs:
        found = analyzer.analyze(job)
        print(f"- {job} ({len(found)} kompetenser)")
        for s in found:
            print(f"    - {s}")

    # Fråga om matchning
    if input("\nVill du matcha dina egna kompetenser? (j/n): ").strip().lower() != "j":
        return

    user = [s.strip() for s in input(
        "Dina kompetenser (kommaseparerade): ").split(",") if s.strip()]
    if not user:
        print("Inga kompetenser angivna.")
        return

    print()
    for job in jobs:
        r = analyzer.match(job, user)
        percent = f"{r['percent']}%" if r["percent"] is not None else "–"
        print(f"--- {job} ---")
        print(f"  Matchning: {percent}")
        print(f"  Matchande: {', '.join(r['matching']) or '–'}")
        print(f"  Saknade:   {', '.join(r['missing']) or '–'}")
        print()


def main():
    analyzer = JobAnalyzer(SKILLS)

    while True:
        print("\n=== AI Job Analyzer ===")
        print("1. Analysera lokala annonser")
        print("2. Analysera AI-jobb från API")
        print("3. Avsluta")

        choice = input("Välj (1-3): ").strip()

        if choice == "1":
            analyze_and_match(load_local_jobs(), analyzer)
        elif choice == "2":
            analyze_and_match(load_api_jobs(), analyzer)
        elif choice == "3":
            print("Hej då!")
            break
        else:
            print("Ogiltigt val.")


if __name__ == "__main__":
    main()
