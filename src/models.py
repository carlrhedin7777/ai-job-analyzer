# models.py


# models.py


class JobAd:
    """En jobbannons."""

    def __init__(self, ad_id, title, company, location, description):
        self.ad_id = ad_id
        self.title = title
        self.company = company
        self.location = location
        self.description = description

    def has_skill(self, skill):
        """Returnerar True om kompetensen finns i annonsen."""
        return skill.lower() in self.description.lower()

    def __str__(self):
        return f"{self.title} hos {self.company} ({self.location})"


class AIJob(JobAd):
    """En AI-specifik jobbannons. Ärver från JobAd."""

    def __init__(self, ad_id, title, company, location, description, ai_area):
        super().__init__(ad_id, title, company, location, description)
        self.ai_area = ai_area

    def __str__(self):
        return f"[AI] {super().__str__()} - {self.ai_area}"


class Candidate:
    """En jobbsökande med kompetenser."""

    def __init__(self, name, skills):
        self.name = name
        self.skills = set(s.lower() for s in skills)

    def __str__(self):
        return f"{self.name} ({len(self.skills)} kompetenser)"


class JobAnalyzer:
    """Analyserar jobbannonser mot en lista av kompetenser."""

    def __init__(self, skills):
        self.skills = skills

    def analyze(self, job):
        """Returnerar en lista av kompetenser som finns i annonsen."""
        return [s for s in self.skills if job.has_skill(s)]

    def match(self, job, candidate):
        """Returnerar matchning mellan kandidat och annons."""
        required = set(s.lower() for s in self.analyze(job))
        matching = required & candidate.skills
        missing = required - candidate.skills

        if not required:
            percent = 0.0
        else:
            percent = round(len(matching) / len(required) * 100, 1)

        return {
            "matching": sorted(matching),
            "missing": sorted(missing),
            "percent": percent,
        }
