# AGENTS.md

## Obiettivo del repository

Questo repository studia la domanda:

> Esiste un algoritmo deterministico in tempo polinomiale per risolvere esattamente il problema del commesso viaggiatore (TSP) in generale?

L'obiettivo è costruire una pipeline di agenti che raccolga, classifichi e valuti la letteratura scientifica sul TSP, con attenzione alla distinzione tra:

- TSP generale;
- TSP metrico;
- TSP euclideo;
- TSP planare;
- casi speciali e grafi particolari;
- algoritmi esatti, approssimati e PTAS.

## Principi generali per tutti gli agenti

1. Non affermare che un problema è in P o NP-hard senza riportare la fonte corretta.
2. Distinguere sempre tra:
   - algoritmo esatto generale;
   - algoritmo speciale;
   - algoritmo approssimato;
   - risultato empirico.
3. Considerare la differenza tra teoria della complessità e performance empirica.
4. Preferire fonti canoniche: paper classici, conferenze e riviste, risultati ampiamente citati.
5. Quando si parla di complessità, indicare sempre la convenzione di input, la metrica e le assunzioni sul grafo.
6. Se un risultato è ambiguo, riportare la distinzione tra "caso generale" e "caso speciale".
7. I report devono essere sintetici ma evidenziare le ipotesi, i teoremi e i limiti.

## Classificazione da usare

Ogni agente deve classificare il risultato in una delle seguenti categorie:

- EXACT_GENERAL: algoritmo esatto per il TSP generale.
- EXACT_SPECIAL: algoritmo esatto per classi particolari.
- APPROX: algoritmo di approssimazione.
- PTAS: schema di approssimazione polinomiale.
- HARDNESS: risultato di NP-hardness o lower bound.
- EMPIRICAL: studio sperimentale senza dimostrazione teorica.

## Output atteso

Per ciascun paper o risultato, l'agente deve produrre almeno:

- titolo e autore;
- anno;
- problema specifico;
- ipotesi sul grafo/metrica;
- complessità dichiarata;
- tipo di approccio;
- conclusione scientifica;
- eventuale criticità o ambiguità.

## Fonti di riferimento consigliate

- Cook (1971) e teoria della NP-completezza;
- Karp (1972) e riduzioni;
- Garey e Johnson, problemi di complessità;
- Held-Karp per il TSP esatto su DP;
- Applegate, Bixby, Chvátal, Cook per TSP combinatorico;
- letteratura su TSP metrico, euclideo e planare;
- paper su PTAS e approssimazioni.

## Comportamento degli agenti custom

I custom agents di questo repository devono:

- essere orientati alla verifica, non alla conclusione a priori;
- usare la ricerca bibliografica come prima fase;
- riportare evidenze concrete e non supposizioni;
- separare sempre teoria da benchmark;
- produrre un report strutturato, non un semplice riassunto libero.

## Prompt standard per i task di ricerca

"Analizza il problema in termini di TSP generale, casi speciali, riduzioni e complessità. Evidenzia se il risultato è esatto, approssimato o empirico. Riferisci le assunzioni e i limiti. Confronta il caso generale con sottoclassi trattevoli."

## Regola finale

Il repository non cerca una risposta magica, ma un sistema coerente per capire se la domanda ha un fondamento teorico solido, se è una falsa speranza algoritmica o se dipende da classi di istanze particolari.
