# Proposta di rifattorizzazione: da pipeline di ricerca a articolo scientifico con algoritmo

## Obiettivo

La pipeline attuale è orientata alla bibliografia e alla classificazione. Per trasformare il progetto in un vero articolo scientifico, occorre cambiare il punto di vista: non più solo "raccogliere evidenze", ma "proporre e valutare un metodo".

L'idea è fare della repository una base per un paper che presenti:

- un problema definito;
- una proposta algoritmica concreta;
- un modello di assunzione chiaro;
- una prova di correttezza o una motivazione teorica iniziale;
- un benchmark comparativo;
- una discussione critica dei limiti.

## Direzione strategica

La pipeline va rifattorizzata in tre livelli:

1. letteratura: restano i moduli di raccolta e classificazione;
2. algoritmo: nasce un modulo dedicato alla proposta di soluzione;
3. articolo: nasce un layer di generazione del documento scientifico.

## Nuova struttura del repository

```text
P_vs_NP/
├── README.md
├── AGENTS.md
├── TODO.md
├── docs/
│   ├── fase1-fondazione.md
│   ├── fase2-bibliografia.md
│   ├── fase3-parsing-normalizzazione.md
│   ├── fase4-analisi-letteratura.md
│   ├── fase5-sviluppo-agenti.md
│   ├── fase6-valutazione-algoritmi.md
│   ├── fase7-sintesi-finale.md
│   ├── fase8-checklist-chiusura.md
│   ├── articolo-proposta-algoritmo.md
│   └── presentazione-progetto.md
├── pipeline/
│   ├── agents/
│   ├── collectors/
│   ├── extractors/
│   ├── classifiers/
│   ├── synthesizers/
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── base_solver.py
│   │   ├── restricted_tsp_solver.py
│   │   └── benchmark_runner.py
│   ├── paper/
│   │   ├── sections/
│   │   ├── manuscript.md
│   │   └── template.md
│   └── orchestrator.py
├── data/
│   ├── initial_tsp_corpus.json
│   ├── literature_claims.json
│   ├── benchmark_template.json
│   └── experiments/
└── run_tsp_pipeline.py
```

## Algoritmo da proporre

Per non partire da una promessa impossibile, la proposta più sensata è di presentare un algoritmo per una classe specifica del problema, non per il caso generale.

### Esempio di proposta concreta

Titolo plausibile:

"A branch-and-bound decomposition method for restricted metric TSP instances"

oppure:

"Exact decomposition heuristic for structured Euclidean TSP instances"

Questa scelta è più credibile perché:

- non pretende di risolvere il TSP generale in tempo polinomiale;
- mantiene la distanza con la qualità scientifica dei risultati canonici;
- si appoggia a un'ipotesi chiara: metriche strutturate, grafi particolari, casi vincolati;
- facilita il benchmarking comparativo e la discussione dei limiti.

## Struttura del paper

### Abstract

- problema;
- approccio;
- assunzioni;
- risultati principali;
- limiti.

### Introduction

- motivazione;
- diffusa distinzione tra TSP generale e casi speciali;
- posizione del lavoro rispetto a letteratura canonica.

### Related work

- Held-Karp;
- Christofides;
- Arora;
- casi speciali geometrici e strutturali.

### Problem definition

- definizione formale del problema;
- assunzioni di grafo e metrica;
- dominio di applicazione.

### Proposed algorithm

- idea principale;
- decomposizione del problema;
- regole di riduzione;
- criteri di pruning;
- pseudo-codice;
- complessità prevista.

### Correctness considerations

- discussione del perché la decomposizione preserva soluzioni ammissibili;
- eventuali condizioni di validità;
- limiti del metodo.

### Experiments

- benchmark su istanze generate;
- confronto con metodi esatti e approssimati;
- misure di tempo e precisione;
- risultati e interpretazione.

### Discussion

- dove il metodo è forte;
- dove fallisce;
- perché non è una soluzione al caso generale.

### Conclusion

- sintesi dei risultati;
- implicazioni per il caso speciale trattato;
- prospettive future.

## Modello di progettazione dell'algoritmo

L'algoritmo va pensato come una classe Python di riferimento:

- `BaseSolver`
- `RestrictedTSPSolver`
- `BenchmarkRunner`

Esempio di API:

```python
solver = RestrictedTSPSolver(instance)
solution = solver.solve()
metrics = solver.metrics()
```

### Funzioni richieste

- parse instance
- compute lower bound
- branch on candidate edges
- prune invalid states
- evaluate final route
- return statistics

## Regola di prudenza scientifica

La proposta non deve mai confondere:

- algoritmo su caso speciale;
- algoritmo approssimato;
- algoritmo esatto generale;
- benchmark empirico.

Se il lavoro vuole essere formalmente credibile, deve dichiarare chiaramente: "il metodo è progettato per una sottoclasse del TSP, non per il caso generale".

## Beneficio del rifactoring

Con questo rifactoring, la repo diventa:

- più coerente dal punto di vista scientifico;
- più vicina a un vero articolo di ricerca;
- più utile come base di presentazione e discussione;
- più simulabile in benchmarking e in validazione empirica.

## Conclusione

Sì, è possibile. La chiave è trasformare la pipeline da "raccolta di evidenze" a "motore di un articolo scientifico". Il punto essenziale è proporre un algoritmo per una classe del problema definita e dichiarata, piuttosto che presentare una soluzione universale che non ha fondamento nel modello di input e nella letteratura.
