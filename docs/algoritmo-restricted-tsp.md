# Algoritmo prototipo: restricted Euclidean TSP

## Obiettivo

Questo documento descrive il prototipo algoritmico sviluppato per un caso ristretto del TSP, con l'obiettivo di costruire una base credibile per un articolo scientifico senza pretendere di risolvere il caso generale.

## Problema

Si considera un insieme di punti nel piano e si vuole trovare un ciclo Hamiltoniano di minima lunghezza totale.

## Assunzioni

- input geometrico euclideo;
- grafo completo;
- distanza euclidea standard;
- istanze strutturate, non arbitrarie.

## Metodo

Il metodo costruisce un tour iniziale usando la regola del nearest neighbor e poi applica una fase di miglioramento local 2-opt.

### Vantaggi

- semplice da implementare;
- facilmente interpretabile;
- adatto a benchmark preliminari;
- scientificamente coerente per sottoclassi del problema.

### Limiti

- non è un algoritmo esatto per il TSP generale;
- non usa un formalismo di complessità polinomiale per il caso universale;
- la qualità della soluzione dipende dalla geometria e dalla struttura delle istanze.

## Risultato atteso

Il prototipo è utile come base per un paper che discute:

- una sottoclasse del TSP;
- un metodo euristico con ipotesi chiare;
- una valutazione empirica su istanze sintetiche;
- un confronto prudente con risultati della letteratura.

## Conclusione

Il lavoro è coerente con la visione del repository: propone un algoritmo per un caso specifico, senza confondere il risultato con una soluzione generale del problema.
