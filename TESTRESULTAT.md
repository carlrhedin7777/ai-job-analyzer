Testresultat – AI Job Analyzer

Alla tester fungerade som förväntat.

Normal matchning
Programmet räknade ut matchningen korrekt för Python, SQL, Git och Docker.

Versaler
Programmet förstod även kompetenser som skrevs med stora bokstäver, till exempel PYTHON och SQL.

Mellanslag
Programmet hanterade extra mellanslag mellan kompetenser utan problem.

Tom input
Om användaren inte skriver in några kompetenser visas meddelandet "Inga kompetenser angivna."

Fel menyval
Om användaren skriver ett ogiltigt val, till exempel 9, visas "Ogiltigt val."

Saknad JSON-fil
Om JSON-filen saknas visas ett felmeddelande och programmet kraschar inte.

Trasig JSON-fil
Om JSON-filen innehåller fel visas ett felmeddelande och programmet kraschar inte.

Nätverksfel
Om internetanslutningen stängs av visas ett meddelande om nätverksfel istället för att programmet kraschar.

Ingen matchning
Om det inte finns någon matchande kompetens visas "–" istället för felaktigt 0 %.

Slutsats

Programmet fungerar bra både vid normal användning och när något går fel. Det hanterar fel med filer och internet utan att krascha.

Programmet skiljer också korrekt mellan 0 % matchning och att det saknas data.