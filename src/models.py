# models.py


# Representerar en jobbannons.
class JobAd:  # Basklassen
    # Tar emot alla fält en annons har
    def __init__(self, ad_id, title, company, location, description):
        self.ad_id = ad_id
        self.title = title
        self.company = company  # self.x = x sparar varje fält på objektet
        self.location = location
        self.description = description

    # bestämmer hur  objektet ska visas när man printar det.
    def __str__(self):
        return f"{self.title} hos {self.company} ({self.location})"

    # En metod som kollar om en kompetens finns i beskrivningen, den använder.
    def has_skill(self, skill):
        # Returnerar True om kompetensen finns i beskrivningen.
        # self.description istället för att ta emot texten som parameter.
        return skill.lower() in self.description.lower()


# En jobbannons specifikt för AI-roller.

class AIJob(JobAd):  # class AIJob(JobAd): ärver från Basklassen JobAd.

    def __init__(self, ad_id, title, company, location, description, ai_area):
        # Anropar förälder klassens metod, så vi slipper skriva om allt.
        super().__init__(ad_id, title, company, location, description)
        # t.ex "NLP", "Computer Vision", "MLOps" # extra attribut som bara AIJob har.
        self.ai_area = ai_area

    # str överskuggar förälderns str och lägger till [AI] och område.
    def __str__(self):
        return f"[AI] {super().__str__()} - {self.ai_area}"


# Analyserar jobbannonser mot en lista av kompetenser.
class JobAnalyzer:

    # Tar emot en lista av kompetenser vi vill leta efter.
    def __init__(self, skills):

        self.skills = skills

    # Returnerar en lista av kompetenser som finns i annonsen
    # Metoden tar emot vilken JobAd som helst (eller AIJob, eftersom AIJob är en JobAd).
    def analyze(self, job_ad):
        # Skapar en tom lista som tillhör variabeln found
        found = []
        for skill in self.skills:
            if job_ad.has_skill(skill):
                # Lägger till hittade kompetenser i slutet av listan
                found.append(skill)
        return found  # Returnerar de hittade kompetenserna


ad = JobAd(1, "AI Engineer", "TechCorp", "Stockholm",
           "Vi söker Python-utvecklare.")

ai = AIJob(1, "AI Engineer", "TechCorp",
           "Stockholm", "Vi söker Python.", "NLP")
