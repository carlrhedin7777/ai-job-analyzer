# models.py
# models.py


class JobAd:  # Basklassen
    def __init__(self, ad_id, title, company, location, description, extra_keywords=None):
        self.ad_id = ad_id
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.extra_keywords = extra_keywords or []

    def full_text(self):
        """Returnerar all text om annonsen som en sträng."""
        parts = [self.title, self.company, self.location, self.description]
        parts.extend(self.extra_keywords)
        return " ".join(parts)

    def has_skill(self, skill):
        """Kollar om kompetensen finns någonstans i annonsen."""
        return skill.lower() in self.full_text().lower()

    def __str__(self):
        return f"{self.title} hos {self.company} ({self.location})"


class Candidate:
    """Representerar en jobbsökande med sina kompetenser."""

    def __init__(self, name, skills):
        self.name = name
        self.skills = set(s.lower() for s in skills)

    def __str__(self):
        return f"{self.name} ({len(self.skills)} kompetenser)"


class AIJob(JobAd):  # Ärver från JobAd
    def __init__(self, ad_id, title, company, location, description, ai_area):
        super().__init__(ad_id, title, company, location, description)
        self.ai_area = ai_area  # t.ex. "NLP", "Computer Vision", "MLOps"

    def __str__(self):
        return f"[AI] {super().__str__()} - {self.ai_area}"


class JobAnalyzer:
    """Analyserar jobbannonser mot en lista av kompetenser."""

    def __init__(self, skills):
        self.skills = skills

    def analyze(self, job_ad):
        """Returnerar en lista av kompetenser som finns i annonsen."""
        found = []
        for skill in self.skills:
            if job_ad.has_skill(skill):
                found.append(skill)
        return found

    def match(self, job_ad, candidate):
        """Jämför kandidatens kompetenser med annonsen."""
        required = set(s.lower() for s in self.analyze(job_ad))
        user = candidate.skills

        matching = required & user
        missing = required - user

        if len(required) == 0:
            percent = 0.0
        else:
            percent = round(len(matching) / len(required) * 100, 1)

        return {
            "matching": sorted(matching),
            "missing": sorted(missing),
            "percent": percent,
            "required_count": len(required),
        }
