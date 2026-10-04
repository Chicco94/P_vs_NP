# Fase 1 - Fondazione del progetto

## Domanda scientifica principale

> Esiste un algoritmo deterministico in tempo polinomiale per risolvere esattamente il problema del commesso viaggiatore (TSP) in generale?

Questa domanda va letta come una questione di teoria della complessità e di algoritmi esatti. Non si tratta semplicemente di trovare un algoritmo efficiente in pratica, ma di capire se il TSP generale ammette una soluzione esatta in tempo polinomiale, oppure se la sua complessità intrinseca la distinzione tra P e NP.

## Confini del progetto

Il progetto non cerca una risposta magica, ma un sistema coerente per:

- distinguere il TSP generale da casi speciali;
- verificare la letteratura canonica sul TSP;
- classificare risultati teorici, approssimativi e empirici;
- identificare limiti, ipotesi e assunzioni del modello;
- sintetizzare un report scientificamente prudente.

## Casi di studio del TSP da analizzare

1. TSP generale
   - grafo pesato completo o non completo;
   - metriche arbitrarie;
   - caso decisionale e di ottimizzazione.

2. TSP metrico
   - distanza che soddisfa triangolare;
   - proprietà di geometricità e approssimazione.

3. TSP euclideo
   - punti nel piano o nello spazio euclideo;
   - vincoli geometrici specifici.

4. TSP planare
   - grafi planar o strutture geometriche con proprietà topologiche.

5. Casi speciali e grafi particolari
   - asimmetrico;
   - simmetrico;
   - grafi con struttura aggiuntiva;
   - canali, nodi vincolati, metriche speciali.

6. Approcci teorici e empirici
   - algoritmi esatti (DP, branch and bound);
   - approssimazioni;
   - PTAS/FPTAS;
   - algoritmi euristici e benchmark sperimentali.

## Struttura del repository

- README.md: descrizione del progetto e obiettivo generale
- TODO.md: piano operativo del progetto
- AGENTS.md: regole per i custom agents
- .github/chatmodes/: agenti custom di VS Code
- .github/prompts/: prompt di supporto alla ricerca
- pipeline/: modulo per raccolta, normalizzazione e reportistica
- docs/: documentazione di progetto e definizione della fondazione

## Documentazione iniziale per la presentazione

La presentazione iniziale del progetto deve chiarire:

- il problema di fondo;
- la differenza tra caso generale e casi speciali;
- la distinzione tra teoria della complessità e benchmarking pratico;
- la metodologia della pipeline di ricerca e analisi.

## Conseguenze pratiche della fondazione

Questo primo step stabilisce:

- il perimetro scientifico del lavoro;
- la definizione dell'oggetto di studio;
- la struttura di sviluppo del repository;
- la base su cui costruire agenti, raccolta bibliografica e classificazione dei paper.
