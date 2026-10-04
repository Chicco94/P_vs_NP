# Un prototipo algoritmico per il TSP euclideo ristretto

## Abstract

Questo documento presenta un prototipo di algoritmo per una sottoclasse del problema del commesso viaggiatore (TSP) in cui i punti sono distribuiti nel piano euclideo e la distanza tra i nodi è definita mediante la metrica Euclidea standard. L'obiettivo non è dimostrare una soluzione esatta per il caso generale, ma costruire un metodo coerente, implementabile e verificabile per istanze geometriche strutturate. Il metodo combina una costruzione iniziale di tipo nearest-neighbor con una fase di ottimizzazione locale 2-opt. L'approccio è inteso come base scientifica per una discussione articolata su esperimenti, assunzioni e limiti, senza confondere il caso ristretto con il TSP generale.

## 1. Introduzione

Il problema del commesso viaggiatore è centrale nella teoria della complessità e nella ricerca operativa. In forma generale, il TSP richiede di trovare un ciclo Hamiltoniano di peso minimo in un grafo completo con pesi arbitrari. La versione generale è ben nota per la sua complessità computazionale, mentre molti risultati teorici e empirici sono disponibili per classi speciali, in particolare per casi geometrici e metrici.

L'obiettivo di questo lavoro non è sostenere che esista un algoritmo esatto e polinomiale per il TSP generale. Al contrario, si propone un metodo progettato per un caso specifico: input euclidei in due dimensioni, con struttura geometrica abbastanza regolare da consentire un approccio euristico leggero ma trasparente.

La scelta di un problema ristretto è motivata da due esigenze. In primo luogo, consente un framing scientificamente corretto: il metodo non pretende di risolvere il caso generale. In secondo luogo, rende possibile una pipeline di sperimentazione realistico, con benchmark sintetici, analisi di costo computazionale e confronto con una baseline di semplice implementazione.

## 2. Definizione del problema

Si consideri un insieme di punti P = {p1, ..., pn} in R^2. Un tour è un ordine di visita di tutti i punti, e la lunghezza del tour è la somma delle distanze euclidee tra punti consecutivi. L'obiettivo è trovare un ciclo Hamiltoniano di lunghezza minima:

$$
T^* = \arg\min_{T} \sum_{(i,j) \in T} \|p_i - p_j\|_2.
$$

La formulazione matematica è standard per il TSP euclideo, ma il metodo proposto non assume che la struttura geometrica sia sufficiente per garantire ottimalità esatta in tutti i casi. L'algoritmo è invece interpretabile come soluzione euristica per una sottoclasse di istanze geometriche.

## 3. Assunzioni e ambito del modello

Il metodo proposto si basa su una serie di assunzioni esplicite:

- input geometrico euclideo;
- grafo completo su punti del piano;
- distanza euclidea standard;
- istanze con una certa regolarità geometrica;
- obiettivo pratico di costruire una soluzione di buona qualità, non necessariamente ottima.

Queste assunzioni comportano un cambiamento di prospettiva rispetto al TSP generale: si abbandona la pretesa di universalità e si accetta un modello di lavoro più realistico e più aderente alla natura empirica del problema.

## 4. Metodo proposto

Il metodo proposto è una combinazione di due fasi:

1. costruzione di un tour iniziale mediante nearest-neighbor;
2. miglioramento locale con la tecnica 2-opt.

La prima fase genera un ciclo ammissibile seguendo la regola "scegli il punto più vicino". La seconda fase riduce la lunghezza del tour esaminando inversioni locali di segmenti e preservando la validità del ciclo.

### 4.1 Costruzione iniziale

A partire da un punto iniziale scelto arbitrariamente, il metodo seleziona iterativamente il punto non ancora visitato più vicino al punto corrente e lo aggiunge al tour. Il risultato è un ciclo Hamiltoniano ammissibile, non necessariamente ottimo.

### 4.2 Miglioramento locale

La fase 2-opt controlla coppie di archi del tour e tenta di migliorare la soluzione invertendo un segmento intermedio. Se la configurazione ottenuta riduce la lunghezza totale, la modifica viene accettata. Il processo viene iterato fino a quando non esiste più un miglioramento locale.

### 4.3 Pseudocodice

```text
Input: insieme di punti P = {p1, ..., pn} in R^2
Output: ciclo Hamiltoniano T

1. S <- {p1, ..., pn}
2. T <- []
3. current <- punto iniziale scelto arbitrariamente in S
4. while S \ {current} non vuoto:
5.     next <- punto in S \ {current} più vicino a current
6.     append next a T
7.     current <- next
8. end while
9. append punto iniziale a T per chiudere il ciclo
10. migliorato <- true
11. while migliorato:
12.     migliorato <- false
13.     for each coppia di archi (i, j), (k, l) in T:
14.         if 2-opt migliora la lunghezza totale:
15.             invertire il segmento tra j e k
16.             migliorato <- true
17.         end if
18.     end for
19. end while
20. return T
```

## 5. Osservazioni sulla complessità e sulla correttezza

La fase nearest-neighbor può essere implementata in modo semplice con un controllo sulle distanze tra il punto corrente e i punti ancora non visitati. La complessità dipende da come vengono aggiornate le distanze e dalla struttura dei dati usati, ma il punto chiave è che il metodo è progettato per applicazioni pratiche, non per una dimostrazione teorica di ottimalità per il caso generale.

La fase 2-opt introduce una procedura di miglioramento locale. In letteratura, tecniche di questo tipo sono ampiamente usate in problemi di routing e ottimizzazione combinatoria, ma non vanno confuse con algoritmi esatti per il TSP generale. Il metodo proposto è quindi da interpretarsi come euristica geometrica per un dominio ristretto, non come soluzione universale.

## 6. Protocollo sperimentale

Il prototipo può essere valutato su istanze sintetiche di punti euclidei con diversa dimensione e struttura geometrica. Un protocollo plausibile include:

- punti distribuiti casualmente nel quadrato unitario;
- istanze con cluster geometrici;
- punti su griglie o forme regolari;
- benchmark con n crescente.

Per ciascuna istanza, si possono registrare:

- lunghezza totale del tour;
- tempo di esecuzione;
- numero di iterazioni 2-opt;
- varianza rispetto a una soluzione di riferimento.

L'analisi sperimentale ha valore soprattutto come verifica empirica della stabilità del metodo in domini geometrici specifici, e non come prova di performance universali.

## 7. Discussione

Il principale vantaggio del metodo è la sua trasparenza: è facile da implementare, facile da spiegare e facile da testare. Inoltre, il suo framing è corretto dal punto di vista scientifico: si presenta come algoritmo per una sottoclasse del TSP, non come soluzione del problema generale.

I limiti sono altrettanto chiari. In generale, una soluzione costruita con nearest-neighbor e 2-opt non è ottima, e non esiste una garanzia teorica di ottimalità per grafi arbitrari o input non geometrici. La validità del metodo dipende dalle ipotesi sul dominio di applicazione e dalla struttura delle istanze considerate.

## 8. Conclusione

Questo documento costruisce una base coerente per un articolo scientifico orientato a una versione speciale del TSP. L'algoritmo presentato non pretende di risolvere il caso generale in tempo polinomiale e non pretende di essere esatto su tutte le istanze. Piuttosto, il suo valore risiede nella chiarezza del modello, della metodologia e delle ipotesi, oltre che nella possibilità di valutazione empirica su classi geometriche specifiche.

In questo senso, il lavoro si inserisce in una prospettiva rigorosa: dimostra che una soluzione concreta, verificabile e documentata può essere sviluppata anche quando il problema da risolvere è un caso ristretto del TSP, senza forzare il quadro teorico o distorcere le conclusioni scientifiche.
