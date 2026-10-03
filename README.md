# AI Job Analyzer

Python-program som analyserar jobbannonser inom AI/IT och matchar dem mot användarens kompetenser.

**Kurs:** Utveckling med Python – grundnivå  
**Roll:** AI Engineer  
**Författare:** Carl Rhedin  
**Datum:** Oktober 2026


## Mål

Bygga ett program som:

- Läser jobbannonser från JSON och API
- Hittar tekniska kompetenser i annonserna
- Matchar användarens kompetenser mot annonserna

Koppling till AI-utvecklarrollen: att hantera extern data, rensa text och bygga en enkel analyspipeline – centrala färdigheter som är aktuella i yrket.



## Metod

| Del | Teknik |
|---|---|
| Språk | Python 3 |
| Standardbibliotek | `json`, `re`, `sys`, `pathlib` |
| Externa bibliotek | `requests`, `ftfy` |
| Data | JSON-fil + RemoteOK API |
| OOP | Klasser och arv |
| Felhantering | `try/except` för fil och nätverk |

**Struktur:**


src/
├── models.py       # JobAd, AIJob, JobAnalyzer
├── api_client.py   # Hämtar jobb från RemoteOK
└── main.py         # Meny och flöde


**Klasser och arv:**

- `JobAd` – basklass med titel och beskrivning.
- `AIJob` – ärver från `JobAd`, lägger till AI-område.
- `JobAnalyzer` – analyserar och matchar.

**Matchningsformel:**


matchning = (matchande kompetenser / kompetenser i annonsen) * 100


Vid 0 kompetenser i annonsen visas `–` (ingen data) istället för `0%` (ingen matchning).



## Resultat

**Lokala annonser – matchning med `Python, SQL, Git, Docker`:**


AI Engineer:         44.4%
ML Engineer:         42.9%
Data Scientist:      50.0%


**API-jobb (RemoteOK):**

Majoriteten av AI-jobben innehöll 0 av våra sökta kompetenser. De är ofta produkt, sälj eller annoteringsroller, inte tekniska utvecklarroller.



## Analys

**Vad resultaten visar:**

- "AI-jobb" är ett brett begrepp – titeln säger inte allt.
- Många AI-roller i API:et är affärs- eller stödroller, inte utvecklarroller.
- Att analysera hela annonsen (titel + beskrivning) ger bättre träffar än bara titeln.

**Trender 2026:**

- Generativ AI och LLM:er dominerar.
- MLOps växer – att driftsätta modeller är efterfrågat.
- Python, SQL, Git och Docker är baskompetenser.
- AWS, Azure och Google Cloud är vanligast.

**Vanliga roller:**

AI Engineer, ML Engineer, Data Scientist, Data Engineer, MLOps Engineer.



## Certifikat-koll

| Certifikat | Utfärdare | Nivå |
|---|---|---|
| AWS Certified Machine Learning – Specialty | AWS | Avancerad |
| Azure AI Engineer Associate | Microsoft | Medel |
| Google Professional ML Engineer | Google Cloud | Avancerad |
| TensorFlow Developer Certificate | Google | Medel |
| IBM AI Engineering Professional Certificate | IBM / Coursera | Nybörjare–Medel |

För nybörjare: TensorFlow Developer Certificate eller IBM AI Engineering är bra startpunkter.



## Reflektion

**Gick bra:** Tydlig klassstruktur med arv, robust felhantering, enkel meny.

**Var svårt:** Dubbelkodad UTF-8 från API:et (löstes med `ftfy`), HTML i beskrivningar, många API-jobb utan tekniska kompetenser.

**Lärt mig:** Hantera extern data robust, rensa och normalisera text, skilja på "ingen matchning" och "ingen data".

**Skulle göra annorlunda:** Fler kompetenser i listan (LLM, MLOps), fler API:er som komplement.



## GitHub

https://github.com/carlrhedin7777/ai-job-analyzer



## Installation

powershell
git clone https://github.com/carlrhedin7777/ai-job-analyzer.git
cd ai-job-analyzer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/main.py


**Menyval:**

1. Analysera lokala annonser
2. Analysera AI-jobb från API
3. Avsluta

Notebook finns i `notebooks/ai_job_analyzer.ipynb`.