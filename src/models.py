# models.py


# models.py


class JobAd:
    """En jobbannons."""

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def has_skill(self, skill):
        """Returnerar True om kompetensen finns i annonsen."""
        text = f"{self.title} {self.description}"
        return skill.lower() in text.lower()

    def __str__(self):
        return self.title


class AIJob(JobAd):
    """En AI-specifik jobbannons. Ärver från JobAd."""

    def __init__(self, title, description, ai_area):
        super().__init__(title, description)
        self.ai_area = ai_area

    def __str__(self):
        return f"[AI] {super().__str__()}"


class JobAnalyzer:
    """Analyserar jobbannonser mot en lista av kompetenser."""

    def __init__(self, skills):
        self.skills = skills

    def analyze(self, job):
        """Returnerar en lista av kompetenser som finns i annonsen."""
        return [s for s in self.skills if job.has_skill(s)]

    def match(self, job, user_skills):
        """Returnerar matchningsresultat mellan användarens skills och annonsen."""
        required = set(s.lower() for s in self.analyze(job))
        if not required:
            return {"percent": None, "matching": [], "missing": []}

        user = set(s.lower() for s in user_skills)
        matching = required & user
        missing = required - user
        percent = round(len(matching) / len(required) * 100, 1)
        return {"percent": percent, "matching": sorted(matching), "missing": sorted(missing)}
