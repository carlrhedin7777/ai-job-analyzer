# main.py är huvudfilen som kör programmet. Den innehåller menyval och flödet för att analysera jobbannonser.


from models import JobAd, AIJob, JobAnalyzer, Candidate
from api_client import fetch_jobs
import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(__file__))


DATA_FILE = "data/jobads.json"
OUTPUT_FILE = "output/results.json"
SKILLS = ["Python", "SQL", "Git", "Docker", "AWS",
          "TensorFlow", "PyTorch", "Machine Learning", "ML", "NLP",]

# ---------- Inläsning ----------


def load_job_ads(filepath):
    """Läser jobbannonser från JSON. Returnerar en lista av dicts."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Kunde inte läsa {filepath}: {e}")
        return []


def build_jobs(raw_ads, from_api=False):
    jobs = []
    for ad in raw_ads:
        ad_id = ad.get("id", 0)
        title = (ad.get("title") or ad.get("position", "Okänd titel")).strip()
        company = ad.get("company", "Okänt företag").strip()
        location = ad.get("location", "Okänd plats").strip()
        description = ad.get("description", "").strip()
        tags = ad.get("tags", [])
        if tags:
            description += " " + " ".join(tags)

        if from_api:
            jobs.append(AIJob(ad_id, title, company,
                        location, description, ai_area="AI"))
        else:
            jobs.append(JobAd(ad_id, title, company, location, description))
    return jobs


# ---------- Analys ----------

def print_analysis(jobs, analyzer):
    """Skriver ut analys av en lista jobb."""
    for job in jobs:
        found = analyzer.analyze(job)
        print(f"- {job} ({len(found)} kompetenser)")
        for skill in found:
            print(f"    - {skill}")


def print_matches(jobs, analyzer, candidate):
    for job in jobs:
        result = analyzer.match(job, candidate)
        percent = f"{result['percent']}%" if result["percent"] is not None else "–"
        print(f"--- {job} ---")
        print(f"  Matchning: {percent}")
        print(f"  Matchande: {', '.join(result['matching']) or '–'}")
        print(f"  Saknade:   {', '.join(result['missing']) or '–'}")
        if result["note"]:
            print(f"  Not:       {result['note']}")
        print()


def save_results(results, filepath):
    """Sparar analysresultat till JSON."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        payload = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "count": len(results),
            "results": results,
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"Sparat till {filepath}")
    except OSError as e:
        print(f"Kunde inte spara: {e}")


# ---------- Meny ----------

def ask_for_skills():
    """Frågar användaren efter kompetenser."""
    text = input("Ange dina kompetenser (kommaseparerade): ").strip()
    return [s.strip() for s in text.split(",") if s.strip()]


def run_analysis(analyzer, use_api, with_candidate=False):
    """Kör analys på antingen lokal fil eller API."""
    if use_api:
        raw = fetch_jobs(limit=5, ai_only=True)
        jobs = build_jobs(raw, from_api=True)
    else:
        raw = load_job_ads(DATA_FILE)
        jobs = build_jobs(raw, from_api=False)

    if not jobs:
        print("Inga jobb att analysera.")
        return

    if with_candidate:
        skills = ask_for_skills()
        if not skills:
            print("Inga kompetenser angivna.")
            return
        candidate = Candidate("Du", skills)
        print()
        print_matches(jobs, analyzer, candidate)
    else:
        print()
        print_analysis(jobs, analyzer)


def show_menu():
    print()
    print("=== AI Job Analyzer ===")
    print("1. Analysera lokala annonser")
    print("2. Analysera AI-jobb från API")
    print("3. Matcha mina kompetenser (lokala)")
    print("4. Matcha mina kompetenser (API)")
    print("5. Avsluta")
    print()


def main():
    analyzer = JobAnalyzer(SKILLS)

    while True:
        show_menu()
        choice = input("Välj (1-5): ").strip()

        if choice == "1":
            run_analysis(analyzer, use_api=False)
        elif choice == "2":
            run_analysis(analyzer, use_api=True)
        elif choice == "3":
            run_analysis(analyzer, use_api=False, with_candidate=True)
        elif choice == "4":
            run_analysis(analyzer, use_api=True, with_candidate=True)
        elif choice == "5":
            print("Hej då!")
            break
        else:
            print("Ogiltigt val.")


if __name__ == "__main__":
    main()
