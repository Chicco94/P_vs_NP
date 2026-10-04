# Fase 5 - Sviluppo degli agenti

## Obiettivo

In questa fase si implementa la parte operativa del sistema: agenti dedicati alla bibliografia, al parsing, alla classificazione, alla sintesi e alla validazione dei risultati.

## Agenti principali

### 1. BibliographicAgent

Responsabile della raccolta iniziale dei paper sulla base di query mirate.

Compiti:

- riceve una lista di query;
- recupera i risultati da Google Scholar;
- ritorna i record grezzi da normalizzare.

### 2. PaperParserAgent

Responsabile della normalizzazione dei risultati in uno schema standard.

Compiti:

- estrarre titolo, abstract, autori, anno, URL;
- inferire problema, assunzioni e complessità;
- creare un record coerente da confrontare tra paper.

### 3. ClassifierAgent

Responsabile della classificazione di ogni paper in una categoria scientifica.

Categorie ammesse:

- EXACT_GENERAL
- EXACT_SPECIAL
- APPROX
- PTAS
- HARDNESS
- EMPIRICAL
- UNKNOWN

### 4. SynthesisAgent

Responsabile della sintesi dei risultati raccolti in un report di insieme.

Compiti:

- aggregare i record;
- contare le categorie;
- generare una vista riassuntiva utile per il report finale.

### 5. ValidationAgent

Responsabile della verifica della coerenza del corpus.

Compiti:

- controllare la distribuzione dei paper per categoria;
- evidenziare eventuali squilibri o ambiguità;
- aiutare a distinguere teoria, casi speciali e benchmark.

## Architettura

L'architettura dei custom agent è modellata in modo semplice e componibile:

- `BaseAgent` definisce l'interfaccia comune;
- ogni agente implementa `run(payload)`;
- i risultati vengono passati in pipeline tra diversi agenti.

## File di riferimento

- [pipeline/agents/base_agent.py](pipeline/agents/base_agent.py)
- [pipeline/agents/bibliographic_agent.py](pipeline/agents/bibliographic_agent.py)
- [pipeline/agents/paper_parser_agent.py](pipeline/agents/paper_parser_agent.py)
- [pipeline/agents/classifier_agent.py](pipeline/agents/classifier_agent.py)
- [pipeline/agents/synthesis_agent.py](pipeline/agents/synthesis_agent.py)
- [pipeline/agents/validation_agent.py](pipeline/agents/validation_agent.py)

## Output atteso della fase 5

Alla fine della fase 5 il progetto deve avere:

- un insieme di agenti reali, non più solo prompt e regole;
- una pipeline minima di elaborazione del corpus;
- una base di classificazione e sintesi pronta per la fase successiva di benchmarking e report finale.
