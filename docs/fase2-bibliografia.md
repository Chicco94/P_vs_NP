# Fase 2 - Raccolta bibliografica

## Query Google Scholar consigliate

Le query seguenti servono come base per una ricerca iniziale e ben contestualizzata:

1. "traveling salesman problem NP-hard"
2. "Hamiltonian cycle NP-complete TSP reduction"
3. "Held-Karp dynamic programming TSP"
4. "metric TSP approximation Christofides"
5. "Euclidean TSP PTAS approximation"
6. "traveling salesman problem special cases polynomial time"
7. "planar TSP polynomial algorithm"
8. "asymmetric TSP complexity"

## Corpus iniziale di riferimento

Il corpus iniziale deve essere limitato ma di alto valore scientifico. La lista seguente è da usare come baseline, non come corpus definitivo.

### 1) TSP generale e hardness

- Held, Karp (1962) - "A Dynamic Programming Approach to Sequencing Problems"
  - categoria: EXACT_GENERAL
  - problema: TSP generale con DP esatto
  - complessità: esponenziale in n, classica O(n^2 2^n)
  - osservazione: è un algoritmo esatto, non polinomiale in generale

- Karp (1972) - "Reducibility Among Combinatorial Problems"
  - categoria: HARDNESS
  - problema: NP-completezza e riduzioni
  - osservazione: fornisce la base per la complessità del TSP generale via riduzioni da Hamiltonian Cycle

- Garey, Johnson (1979) - "Computers and Intractability"
  - categoria: HARDNESS
  - problema: complessità di problemi combinatori, incluso TSP
  - osservazione: riferimento canonico per il quadro di NP-hardness e riduzioni

### 2) Approssimazioni metriche

- Christofides (1976) - "Worst-Case Analysis of a New Heuristic for the Travelling Salesman Problem"
  - categoria: APPROX
  - problema: TSP metrico
  - approccio: 1.5-approximation
  - osservazione: risultato classico per metric TSP, ma non risolve il caso generale esattamente

### 3) PTAS per casi geometrici

- Arora (1998) - "Polynomial Time Approximation Schemes for Euclidean TSP and other Geometric Problems"
  - categoria: PTAS
  - problema: TSP euclideo
  - approccio: PTAS
  - osservazione: risultato teorico fondamentale per geometria e approssimazione, non per TSP generale

- Mitchell (1999) - "Guillotine Subdivisions Approximate Polygonal Regions in..."
  - categoria: PTAS
  - problema: TSP euclideo e geometrico
  - osservazione: risultato correlato di PTAS nel quadro euclideo

### 4) Casi speciali e grafi particolari

- TSP planare / casi strutturali specifici
  - categoria: EXACT_SPECIAL
  - osservazione: questi casi vanno studiati separatamente poiché non generalizzano il TSP generale

- TSP asimmetrico e varianti speciali
  - categoria: EXACT_SPECIAL / APPROX
  - osservazione: la complessità e gli algoritmi cambiano in modo sensibile rispetto al caso simmetrico

## Criteri per la qualità di un paper

Un paper va considerato rilevante se:

- è classico o ampiamente citato;
- specifica chiaramente la metrica e le ipotesi;
- distingue tra caso generale e caso speciale;
- esplicita la complessità o la garanzia di approssimazione;
- non confonde performance empirica con risultato teorico.

## Output atteso della fase 2

Alla fine della fase 2 il repository deve contenere:

- una lista iniziale di query rilevanti;
- un corpus minimo di paper chiave;
- una classificazione preliminare della letteratura;
- una distinzione tra risultati canonici, supportivi e marginali.

## Nota metodologica

La ricerca bibliografica non deve essere interpretata come una prova di impossibilità o di esistenza di un algoritmo polinomiale. Il suo compito è costruire una base di evidenza su cui confrontare i risultati teorici, gli approcci specializzati e i benchmark sperimentali.
