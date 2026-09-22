# main.py

# En hårdkodad jobbannons (så länge)
job_ad = """
Vi söker en AI Engineer till vårt team i Stockholm.
Du kommer att arbeta med Python, TensorFlow och PyTorch.
Erfarenhet av Machine Learning och NLP är meriterande.
Vi använder Docker, Git och AWS i vår dagliga utveckling.
SQL-kunskaper är ett krav.
"""


# Kompetenskrav, Kompeteskrav vi letar efter - En lista med strängar
skills_to_find = [
    "Python",
    "SQL",
    "Git",
    "Docker",
    "AWS",
    "TensorFlow",
    "PyTorch",
    "Machine Learning",
    "NLP",
]
print(skills_to_find)

# Funktion som returnerar en lista med de kompetenser som finns i texten.


def find_skills(text, skills):
    # en tom lista där vi samlar det vi hittar.
    found = []
    # loopar igenom varje kompetens.
    for skill in skills:
        # kollar om kompetensen finns i texten. lower() för att ignorera skiftläge. (python och Python)
        if skill.lower() in text.lower():
            # lägger till kompetensen i listan
            found.append(skill)
    # skickar tillbaka listan.
    return found


# Använd funktionen för att hitta kompetenser i jobbannonsen
found_skills = find_skills(job_ad, skills_to_find)
print("Kompetenser som hittades:")
for skill in found_skills:
    print(f"- {skill}")
