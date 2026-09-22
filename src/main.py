# main.py

# Hämtar json-modulen för att kunna läsa JSON-filer.
import json

# En ny funktion, filepath är sökvägen till filen som ska läsas.
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


# Definierar en lista med skills som ska sökas efter i jobbannonserna.
skills_to_find = [
    "Python", "SQL", "Git", "Docker", "AWS",
    "TensorFlow", "PyTorch", "Machine Learning", "NLP",
]


# Funktionen returnerar en lista med de färdigheter som finns i texten.
def find_skills(text, skills):
    found = []
    for skill in skills:
        if skill.lower() in text.lower():
            found.append(skill)
    return found


# Huvudflöde
# Läser in jobbannonser från filen "data/jobads.json" och lagrar dem i variabeln job_ads.
job_ads = load_job_ads("data/jobads.json")

# Skriver ut antalet annonser som har lästs in från filen.
print(f"Antal annonser: {len(job_ads)}")
print()

# Loopar igenom varje annons i listan
for ad in job_ads:
    # Hämtar fält från dict: ad['title'] osv. En f-sträng sätter in dem i texten. 
    print(f"--- {ad['title']} hos {ad['company']} ({ad['location']}) ---")
    # Använder vår gamla funktion på den nya datan.
    found = find_skills(ad["description"], skills_to_find)
    for skill in found:    
        print(f"  - {skill}")
    print()
