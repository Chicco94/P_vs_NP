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

## Agenti custom per VS Code

Nel repository sono stati definiti agenti custom da usare direttamente con GitHub Copilot in VS Code:

- TSP Researcher: ricerca bibliografica, classificazione dei paper e sintesi scientifica.
- TSP Validator: benchmark e verifica empirica di algoritmi esatti e approssimati.
- TSP Orchestrator: ciclo iterativo di recupero evidenze, miglioramento della dimostrazione, aggiornamento del report e compilazione del PDF.
- TSP Algorithm Synthesizer: analisi critica dei paper integrali e sviluppo/verifica di un candidato algoritmico originale.
- prompt di review della letteratura: scaffolding per valutare rapidamente un nuovo paper.

### Task runner per l'orchestratore

Il progetto include anche un runner unico per avviare il ciclo completo:

```powershell
python run_tsp_pipeline.py --queries "TSP NP-hardness" "Held Karp TSP exact algorithm" --max-results 2 --iterations 2
```

oppure in modalità target singolo:

```powershell
python run_tsp_pipeline.py --target "TSP NP-hardness" --max-results 3 --iterations 4
```

Il runner raccoglie le fonti; l'agente orchestratore deve analizzarne il testo integrale e sintetizzare un nuovo algoritmo candidato. Le pubblicazioni sono evidenza e materiale di partenza, non la soluzione richiesta. Il runner Python non genera autonomamente algoritmi: il custom agent di VS Code svolge la fase di sintesi e registra il candidato in `pipeline/output/algorithm_candidate.json`.

I documenti raccolti vengono accumulati tra esecuzioni nel file `pipeline/output/paper_corpus.json`. Al primo avvio, se il corpus non esiste, il runner importa i record dal report precedente `pipeline/output/q_orchestrator_report.json`. I risultati ripetuti vengono uniti usando titolo e anno, evitando di creare duplicati; il percorso si può cambiare con `--corpus`.

Se Windows o OneDrive blocca temporaneamente il file durante il salvataggio, il runner ritenta la sostituzione. Se il lock persiste, conserva l'aggiornamento in uno snapshot `paper_corpus.pending-*.json` e lo recupera automaticamente alla successiva esecuzione.

Il candidato è un artefatto separato dalle schede bibliografiche. Il runner accetta `--algorithm-candidate` per configurarne il percorso. Il JSON deve contenere `origin`, `pseudocode`, `deterministic`, `exact`, `scope`, `polynomial_time`, `complexity_analysis`, `correctness_argument`, `source_papers`, `verification_status` e `verification_evidence`. `completed` indica che l'agente ha registrato tali verifiche; test empirici da soli non dimostrano correttezza generale o complessità polinomiale. `max_iterations_reached` e `search_stalled` restano esiti inconclusivi.

Se il testo integrale di una fonte non è disponibile legalmente o tramite accesso aperto, l'agente deve segnalarlo e non presentare abstract o metadati come analisi del paper completo.

Questi agenti sono definiti in:

- [AGENTS.md](AGENTS.md)
- [.github/agents/tsp-algorithm-synthesizer.agent.md](.github/agents/tsp-algorithm-synthesizer.agent.md)
- [.github/chatmodes/tsp-researcher.chatmode.md](.github/chatmodes/tsp-researcher.chatmode.md)
- [.github/chatmodes/tsp-validator.chatmode.md](.github/chatmodes/tsp-validator.chatmode.md)
- [.github/chatmodes/tsp-orchestrator.chatmode.md](.github/chatmodes/tsp-orchestrator.chatmode.md)
- [.github/prompts/tsp-literature-review.prompt.md](.github/prompts/tsp-literature-review.prompt.md)

Sono stati pensati per guidare i lavori di ricerca in modo più rigoroso, distinguendo teoria, casi speciali e validazione empirica.
