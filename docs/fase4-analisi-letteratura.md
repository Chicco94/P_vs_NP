# Fase 4 - Analisi della letteratura

## Obiettivo

In questa fase si costruisce la knowledge base dei risultati principali e si distinguono le diverse famiglie di claim scientifici sul TSP.

## Teoremi e risultati canonici da riconoscere

### 1. TSP generale e hardness

- Hamiltonian Cycle è NP-complete
- TSP decisionale è NP-complete
- il TSP di ottimizzazione è NP-hard
- l'esistenza di un algoritmo esatto polinomiale per il TSP generale implica P = NP

### 2. Algoritmi esatti

- Held-Karp dynamic programming
- branch-and-bound classici per il TSP
- algoritmi esatti per casi speciali e grafi particolari

### 3. Approssimazione

- Christofides per TSP metrico: 1.5-approximation
- risultati di approssimazione per TSP asimmetrico e metric variants

### 4. PTAS e geometrici

- Arora per TSP euclideo
- PTAS per problemi geometrici e casi speciali

### 5. Casi speciali e sottoclassi

- TSP euclideo
- TSP metrico
- TSP planare
- TSP su grafi particolari e strutture vincolate

## Classificazione dei risultati

Ogni paper o claim va classificato in una delle seguenti categorie:

- EXACT_GENERAL
- EXACT_SPECIAL
- APPROX
- PTAS
- HARDNESS
- EMPIRICAL

## Knowledge base dei claim scientifici

Per ogni risultato va registrare almeno:

- titolo e autore
- anno
- categoria
- problema specifico
- metrica o ipotesi sul grafo
- complessità dichiarata
- approccio
- eventuale limitazione o ambiguità

## Matrice di confronto

| Categoria | Caso tipico | Obiettivo | Conseguenza scientifica |
| --- | --- | --- | --- |
| EXACT_GENERAL | TSP generale | soluzione esatta | se polinomiale, implicherebbe P = NP |
| EXACT_SPECIAL | casi particolari | soluzione esatta su classi ristrette | non generalizza al caso completo |
| APPROX | TSP metrico | soluzione vicino all'ottimo | non è esatta |
| PTAS | TSP euclideo | schema di approssimazione polinomiale | risultato forte ma solo su classi speciali |
| HARDNESS | riduzioni NP-hard | prova di intrattabilità | non dimostra una soluzione esatta polinomiale |
| EMPIRICAL | benchmark su dati reali | performance pratica | non sostituisce la teoria |

## Regola di prudenza

Un risultato dev'essere interpretato solo nel contesto delle assunzioni del problema. La stessa parola "TSP" può riferirsi a situazioni molto diverse: generale, metrico, euclideo, planare, asimmetrico, eccezioni strutturali.

## Output atteso

Alla fine della fase 4 il repository deve avere:

- una mappa dei risultati canonici;
- una tabella di classificazione;
- una base di claim scientifici pronti per la sintesi finale;
- una chiara separazione tra teoria, casi speciali e benchmark.
