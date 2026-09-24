# main.py

# Importerar våra klasser.
# Hämtar json-modulen för att kunna läsa JSON-filer.
# sys används för att prata med Python-systemet.
# os används för att prata med operativsystemet.
from models import JobAd, AIJob, JobAnalyzer

import json
import sys
import os


# Gör det möjligt att importera models.py även när vi kör main.py
# från projektets rotmapp.
#
# os.path.dirname(__file__) ger sökvägen till mappen där main.py ligger
# (dvs. src).
#
# sys.path.append(...) lägger till den mappen i Pythons lista över
# platser där Python letar efter moduler när vi använder import.
#
# Varför? Utan detta kan Python i vissa körsätt inte hitta models.py
# eftersom den ligger i src.
sys.path.append(os.path.dirname(__file__))


# Funktionen läser jobbannonser från en JSON-fil. Returnerar en lista.
# Felhantering: Om filen inte hittas eller om JSON är ogiltig, returnerar den en tom lista.

# Funktionen tar en parameter, filepath, som är sökvägen till filen som ska läsas.
def load_job_ads(filepath):
    try:
        # Öppnar filen i läsläge med UTF-8-kodning och ger den namnet f.
        with open(filepath, "r", encoding="utf-8") as f:
            # Läser in JSON-data från filen och lagrar den i variabeln data.
            data = json.load(f)
        # Returnerar den inlästa datan (en lista med jobbannonser).
        return data
    except FileNotFoundError:
        # Om filen inte hittas,returneras en tom lista och ett felmeddelande.
        print(f"Filen hittades inte: {filepath}")
        return []
    # Om JSON är ogiltig, returneras en tom lista och ett felmeddelande.
    except json.JSONDecodeError:
        print(f"Filen är inte gilitig JSON: {filepath}")
        return []


# Omvandlar dicts från JSON till JobAd-objekt.
def build_job_objects(raw_ads):
    jobs = []
    for ad in raw_ads:
        # Skapar ett JobAd-objekt i vår class med namngivna argument – tydligare än positionsargument.
        # Namngivna argument eftersom det blir tydligare och lättare att läsa, särskilt när JobAd har flera parametrar.
        # Det minskar också risken att råka lägga ett värde på fel plats.
        job = JobAd(
            ad_id=ad["id"],
            title=ad["title"],
            company=ad["company"],
            location=ad["location"],
            description=ad["description"],
        )
        jobs.append(job)
    return jobs


# Definierar en lista med skills som ska sökas efter i jobbannonserna.
skills_to_find = [
    "Python", "SQL", "Git", "Docker", "AWS",
    "TensorFlow", "PyTorch", "Machine Learning", "NLP",
]

# Skapar en analyzer med vår lista av kompetenser.
analyzer = JobAnalyzer(skills_to_find)


# Huvudflöde
# Läser in jobbannonser från filen "data/jobads.json" och lagrar dem i variabeln job_ads.
raw_ads = load_job_ads("data/jobads.json")
job_objects = build_job_objects(raw_ads)


# Skriver ut antalet annonser som har lästs in från filen.
print(f"Antal annonser: {len(job_objects)}")
print()


# Loopar igenom varje annons i listan
# Går igenom varje jobb i listan job_objects och kalla dem för job.
for job in job_objects:
    print(f"--- {job} ---")
    # Anropar analyzerns metod – den använder job.has_skill() internt.
    found = analyzer.analyze(job)
    for skill in found:
        print(f"  - {skill}")
    print()
