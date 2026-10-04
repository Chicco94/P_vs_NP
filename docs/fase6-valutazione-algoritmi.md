# Fase 6 - Valutazione algoritmi

## Obiettivo

In questa fase si costruisce il primo framework di benchmarking per confrontare algoritmi esatti e approssimati sul TSP, distinguendo chiaramente tra performance empirica e risultati teorici.

## Tipi di istanza da considerare

1. TSP generale casuale
   - grafi pesati completi
   - metriche arbitrarie

2. TSP metrico
   - rispetto triangolare
   - casi standard per approssimazione

3. TSP euclideo
   - punti nello spazio euclideo
   - geometria reale e casi simili a applicazioni pratiche

4. TSP planare o con struttura speciale
   - grafi con vincoli topologici o geometrici

5. Casi speciali e vincolati
   - asimmetrico
   - limitato
   - casi artificiali ma utili per analisi comparativa

## Algoritmi da confrontare

- algoritmo esatto basato su programmazione dinamica
- branch-and-bound classico
- algoritmo di approssimazione metrico (es. Christofides)
- algoritmo PTAS per Euclidean TSP
- euristica semplice come baseline empirica

## Metriche di valutazione

Per ciascun algoritmo va misurato almeno:

- tempo di esecuzione;
- memoria utilizzata;
- qualità della soluzione rispetto all'ottimo;
- scala dei problemi trattabili;
- stabilità dei risultati su diverse istanze.

## Output desiderato

La fase 6 produce:

- benchmark su istanze semplici e complesse;
- confronto tra esatto e approssimato;
- evidenza sul comportamento in casi speciali;
- quadro utile per la sintesi finale e per la presentazione.

## Regola metodologica

Un algoritmo che funziona bene in pratica su un caso speciale non dimostra che il TSP generale sia risolvibile esattamente in tempo polinomiale. Il benchmarking deve sempre riportare il contesto del problema.
