# Fase 3 - Parsing e normalizzazione

## Stack scelto

Per la prima versione del progetto si usa uno stack minimale e trasparente:

- Python 3.x
- `requests` per il recupero di HTML e metadata
- `BeautifulSoup` per il parsing di pagine web e contenuti strutturati
- `pypdf` / `pdfplumber` come estensione futura per PDF

Questo approccio permette:

- di ottenere rapidamente un prototipo funzionante;
- di mantenere il sistema leggibile e facilmente depurabile;
- di separare la fase di raccolta bibliografica da quella di estrazione del contenuto.

## Obiettivo della fase

La fase 3 rende i paper confrontabili tra loro, trasformando i risultati grezzi in una scheda standardizzata.

## Schema standard di paper

Ogni record di paper deve contenere almeno:

- `title`: titolo del lavoro
- `authors`: lista degli autori
- `year`: anno di pubblicazione
- `source`: rivista, convegno o sito di origine
- `url`: URL di riferimento
- `abstract`: abstract o sintesi testuale
- `problem`: tipo di problema trattato
- `assumptions`: lista delle ipotesi sul grafo o sulla metrica
- `complexity`: dichiarazione di complessità
- `approach`: approccio teorico o empirico
- `classification`: categoria scientifica del risultato
- `confidence`: punteggio di affidabilità del riconoscimento
- `notes`: osservazioni critiche e limiti

## Normalizzazione testuale

Prima di classificare un risultato, il testo va normalizzato in modo da evitare errori di confronto tra articoli diversi.

Regole principali:

- lowercase per i test di parole chiave;
- pulizia di spazi, segni di punteggiatura e caratteri speciali;
- rimozione di token irrilevanti in fase di classificazione;
- mapping dei concetti principali in un vocabolario comune:
  - `np-hard`, `hardness`, `approximation`, `ptas`, `exact`, `dynamic programming`, `euclidean`, `metric`, `planar`.

## Modulo di riferimento

Il progetto implementa questa normalizzazione in:

- [pipeline/extractors/paper_extractor.py](pipeline/extractors/paper_extractor.py)
- [pipeline/models.py](pipeline/models.py)

## Standard di output

L'output del parsing viene trasformato in un record strutturato e salvato in JSON e Markdown, così da essere facilmente usato da agenti successivi e da un database di riferimento.

## Criterio di qualità

Un record è valido se:

- ha titolo e abstract non vuoti;
- ha almeno un problema o categoria coerente;
- distingue tra evidenza teorica e empirica;
- conserva la fonte originale e le assunzioni del modello.

## Risultato atteso della fase 3

Alla fine di questa fase il repository deve avere:

- un parser standard per paper;
- uno schema comune di metadata e assunzioni;
- un sistema di normalizzazione per confrontare articoli in modo uniforme;
- una base pronta per la successiva analisi della letteratura.
