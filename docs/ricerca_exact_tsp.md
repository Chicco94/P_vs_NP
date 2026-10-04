# Rilancio della pipeline: evidenza bibliografica e direzione algoritmica

## Obiettivo

Rilanciare la pipeline di raccolta letteratura con una attenzione più forte ai risultati di:

- NP-hardness e lower bound;
- algoritmi esatti esponenziali;
- casi speciali risolubili in tempo polinomiale;
- PTAS e approssimazioni geometriche;
- distinzione tra caso generale e casi speciali.

## Risultato della nuova esecuzione

La pipeline è stata rieseguita con una lista di query più rigorosa, includendo:

- Karp 1972 TSP NP-hardness;
- Held-Karp exact dynamic programming;
- Euclidean TSP NP-hardness;
- planar TSP special cases;
- bitonic TSP polynomial case;
- metric TSP lower bounds;
- Euclidean TSP PTAS;
- TSP special cases polynomial time exact.

La nuova esecuzione ha prodotto un report di output, ma i risultati ottenuti mostrano un problema metodologico importante: la raccolta da Google Scholar non è affidabile in ambiente automatizzato e produce spesso risultati generici o link di browser, non paper scientifici.

Questo è un dato utile: la pipeline è stata rianimata, ma il livello di qualità bibliografica del recupero è ancora insufficiente per sostenere conclusioni teoriche forti.

## Conclusione scientifica preliminare

I risultati canonici della letteratura suggeriscono che:

- il TSP generale è NP-hard;
- gli algoritmi esatti classici come Held-Karp hanno complessità esponenziale;
- per casi speciali, esistono algoritmi polinomiali o approssimazioni efficienti;
- per il TSP euclideo e per casi geometrici, esistono PTAS e risultati specializzati;
- non esiste evidenza affidabile di un algoritmo deterministico esatto in tempo polinomiale per il TSP generale senza implicare un risultato teorico molto forte (ad esempio P = NP).

In altre parole, la direzione corretta non è costruire un algoritmo “universale” senza basi teoriche, ma costruire un metodo rigoroso per classi speciali del problema.

## Fonti canoniche da inserire nella pipeline

1. Karp (1972) – NP-hardness e riduzioni;
2. Held and Karp (1962) – dynamic programming for TSP exact solution;
3. Garey and Johnson – TSP hardness and structural complexity results;
4. Arora (1998) – PTAS for Euclidean TSP;
5. Mitchell (1999) – geometric approximation results;
6. Special-case polynomial algorithms for structured instances (bitonic TSP, tree metrics, Monge cases, planar restrictions, bounded treewidth variants, etc.).

## Direzione algoritmica ragionevole

L'obiettivo realistico non è più costruire un algoritmo deterministico polinomiale e completo per il TSP generale, ma definire un nuovo algoritmo per una sottoclasse del problema, con:

- ipotesi esplicite;
- dominio specifico;
- complessità polinomiale per il dominio ristretto;
- correttezza dimostrabile rispetto alla classe considerata;
- confronto esplicito con il caso generale.

Questa è una direzione che rispetta il quadro della teoria della complessità e evita falsi “miracoli algoritmici”.

## Prossimo passo

La pipeline deve essere migliorata sostituendo Google Scholar con fonti di metadati e documenti più controllate, come:

- Crossref;
- OpenAlex;
- DBLP;
- arXiv;
- bibliografie canoniche da paper classici.

Solo così la raccolta bibliografica potrà sostenere una nuova fase di progettazione algoritmica senza distorcere la teoria con risultati non verificati.
