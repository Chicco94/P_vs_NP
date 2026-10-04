# Fase 7 - Sintesi finale

## Obiettivo

La sintesi finale raccoglie i principali risultati del progetto in un report coerente, distinguendo tra:

- teoria della complessità;
- algoritmi esatti;
- algoritmi approssimati;
- casi speciali;
- evidenze empiriche;
- limiti metodologici.

## Struttura del report finale

### 1. Domanda di ricerca

> Esiste un algoritmo deterministico in tempo polinomiale per risolvere esattamente il problema del commesso viaggiatore (TSP) in generale?

### 2. Esito atteso della ricerca

Il report deve chiarire che:

- il TSP generale è generalmente considerato NP-hard;
- algoritmi esatti esistenti sono esponenziali nel numero di nodi;
- i casi speciali possono essere trattati con metodi più efficienti;
- le approssimazioni e i PTAS non risolvono il problema generale in modo esatto;
- l'esistenza di un algoritmo esatto polinomiale generale sarebbe equivalente a un risultato teorico profondo e con implicazioni su P vs NP.

### 3. Mappa delle evidenze

La mappa deve includere almeno:

- Held-Karp: algoritmo esatto ma esponenziale;
- Karp e Garey-Johnson: hardness e riduzioni;
- Christofides: approssimazione per TSP metrico;
- Arora: PTAS per TSP euclideo.

### 4. Confronto tra casi

Il report deve mettere in evidenza la differenza tra:

- TSP generale;
- TSP metrico;
- TSP euclideo;
- TSP planare;
- casi speciali particolari.

### 5. Limiti metodologici

La sintesi finale deve sottolineare che:

- un benchmark non sostituisce una dimostrazione teorica;
- una buona performance empirica non implica soluzione polinomiale generale;
- un algoritmo specializzato non va generalizzato senza prove specifiche.

## Produce un report prudente

Il report finale deve evitare conclusioni troppo forti. La conclusione più corretta è che il progetto mostra come la letteratura distingua chiaramente tra:

- problemi trattabili in casi speciali;
- algoritmi approssimati e PTAS;
- il TSP generale, che rimane il punto teorico di maggiore interesse e complessità.

## Output atteso

Il risultato della Fase 7 è un documento sintetico, scientificamente prudente e ben separato tra:

- teoremi;
- casi speciali;
- approssimazioni;
- evaluazioni empiriche;
- limiti e ipotesi.
