# P vs NP: ricerca su TSP e algoritmi deterministici

## Obiettivo del progetto

Questo repository nasce come progetto di ricerca e sperimentazione intorno a una domanda centrale della teoria della computazione:

> Esiste un algoritmo deterministico in tempo polinomiale per risolvere esattamente il problema del commesso viaggiatore (TSP) in generale?

L'obiettivo non è solo costruire un algoritmo “miracoloso”, ma sviluppare un sistema di agenti in grado di:

- raccogliere articoli scientifici da fonti come Google Scholar;
- estrarre i risultati chiave dal testo dei paper;
- classificare i risultati in base a dominio, complessità e assunzioni;
- confrontare algoritmi esatti, approssimati e specializzati;
- verificare empiricamente ipotesi su casi particolari del TSP;
- sintetizzare una conclusione scientificamente fondata.

## Domande di ricerca

1. Il TSP generale ammette un algoritmo esatto deterministico in tempo polinomiale?
2. Quali classi di problemi TSP sono risolubili in tempo polinomiale o quasi-polinomiale?
3. Quali risultati di letteratura dimostrano la distinzione tra casi generalizzati e casi speciali?
4. Come si differenziano gli algoritmi esatti da quelli di approssimazione e PTAS?
5. È possibile costruire un agente che rilevi automaticamente i teoremi chiave e li validi empiricamente?

## Ipotesi di lavoro

La ricerca parte da una premessa fondamentale:

- il TSP generale è noto essere NP-hard;
- algoritmi esatti classici (come Held-Karp) hanno complessità esponenziale;
- per casi speciali, esistono algoritmi più efficienti o schemi di approssimazione;
- un algoritmo deterministico polinomiale esatto per il caso generale non è stato trovato, e la sua esistenza è strettamente legata alla relazione tra P e NP.

In altre parole, un risultato “positivo” in senso assoluto potrebbe implicare una svolta nella teoria della complessità, mentre un risultato “negativo” realistico porterebbe a una classificazione rigorosa dei casi trattabili.

## Piano di lavoro

### 1. Raccolta letteratura

- raccolta di articoli scientifici su Google Scholar e fonti accessorie;
- valutazione di titolo, abstract, citazioni e rilevanza scientifica;
- costruzione di un corpus di riferimenti centrali sul TSP.

### 2. Analisi dei paper

- estrazione di dimostrazioni, assunzioni e complessità;
- separazione tra:
  - TSP generale,
  - TSP metrico,
  - TSP euclideo,
  - TSP planare,
  - TSP su grafi speciali,
  - algoritmi di approssimazione e PTAS.

### 3. Struttura dei risultati

- conversione di ogni paper in una scheda normalizzata con:
  - titolo,
  - autore,
  - anno,
  - problema,
  - ipotesi,
  - complessità,
  - approccio,
  - conclusione.

### 4. Sviluppo di agenti

Costruzione di una pipeline composta da agenti dedicati a:

- ricerca bibliografica;
- parsing del testo scientifico;
- estrazione dei claim scientifici;
- confronto e classificazione dei risultati;
- validazione empirica degli algoritmi;
- sintesi finale e report di presentazione.

### 5. Verifica sperimentale

- confronto su grafi piccoli e medi;
- test di algoritmi esatti e approssimati;
- analisi di casi critici e controesempi;
- valutazione della complessità reale dell'implementazione.

### 6. Sintesi finale

- redazione di un report conclusivo;
- mappa dei risultati principali;
- confronto tra le teorie della computazione e i risultati empirici;
- eventuale proposta di algoritmo per una classe speciale del problema.

## Risultati attesi

I risultati più plausibili sono tre:

1. Conclusione teorica: il TSP generale è intrattabile esattamente in tempo polinomiale, salvo dimostrare P = NP.
2. Classificazione dei casi speciali: individuazione di sottoclassi del problema risolubili in tempo polinomiale o con PTAS.
3. Framework di analisi: un sistema automatico capace di leggere la letteratura e organizzare i risultati in modo contestuale.

## Limiti e cautela metodologica

- Google Scholar richiede una gestione attenta del scraping e della compliance.
- La letteratura può contenere risultati molto diversi tra loro, perché il TSP cambia radicalmente in base alle assunzioni sul grafo, sulla metrica e sulla dimensione.
- Un agente deve distinguere nettamente tra:
  - algoritmo esatto generale,
  - algoritmo su caso speciale,
  - algoritmo di approssimazione,
  - risultato puramente empirico.

## Deliverable previsto

Il repository dovrà contenere:

- la codebase per la raccolta e il parsing delle pubblicazioni;
- un database o file strutturato dei paper analizzati;
- script di benchmark e validazione;
- un report finale di sintesi per la presentazione.

## Conclusione

Questo progetto si configura come una ricerca interdisciplinare tra:

- teoria della computazione,
- intelligenza artificiale e agenti,
- recupero delle informazioni,
- analisi empirica e benchmark.

L’enfasi non è solo sull’algoritmo finale, ma sulla capacità di costruire un sistema che sia in grado di comprendere, organizzare e verificare la letteratura scientifica sul problema.
