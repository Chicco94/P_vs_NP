# Pipeline automatica per la ricerca sul TSP

Questa directory definisce una pipeline minimale ma completa per automatizzare la ricerca e la classificazione della letteratura sul TSP.

## Obiettivo

La pipeline deve:

1. cercare paper e riferimenti su Google Scholar usando query mirate;
2. normalizzare i risultati in un formato strutturato;
3. estrarre assunzioni, complessità e approccio;
4. classificare il risultato tra `EXACT_GENERAL`, `EXACT_SPECIAL`, `APPROX`, `PTAS`, `HARDNESS` e `EMPIRICAL`;
5. generare un report sintetico finale.

## Struttura

- `collectors/`: recupero dei risultati da Google Scholar.
- `extractors/`: normalizzazione e parsing del contenuto.
- `classifiers/`: classificazione del risultato scientifico.
- `synthesizers/`: generazione di report in JSON e Markdown.
- `orchestrator.py`: punto di ingresso unico della pipeline.

## Esecuzione

```bash
python pipeline/orchestrator.py --queries "TSP NP-hard" "Held-Karp TSP exact" "Euclidean TSP PTAS"
```

Il comando produce un file JSON nella cartella `pipeline/output/`.

## Nota metodologica

La pipeline è progettata per guidare la raccolta e la sintesi, non per sostituire la verifica umana. In particolare, le conclusioni teoriche vanno sempre confrontate con i paper canonici e con le assunzioni del modello di input.
