# TODOs

## Sviluppo e Funzionalità

- [x] ~~Fissare un messaggio in cima, il bot modifica il testo ogni minuto mostrando l'orario corrente. Se l'orario mostrato è diverso dall'orario attuale, significa che il bot è offline.~~
- [ ] Se viene richiesto un codice con "cat", invia l'immagine con Carbon.
- [ ] Aggiornare help con tutti i nuovi comandi.
- [x] ~~Implementare funzionalità per il comando "cat"~~
    - [x] ~~Inserire un pulsante per "cat" il file sotto ogni messaggio del percorso.~~
    
- [x] ~~Pushare un file inviato da Telegram in una directory specifica.~~

## Baghi

- [ ] Bug nella funzione push quando vengono mandati messaggi da altri utenti (?)

## Ottimizzazione del Codice

- [ ] Migliorare la gestione delle eccezioni:
    - [ ] Gestire i tentativi di connessione all'API di Telegram.
- [x] ~~Migliorare i log con la libreria logging~~
    - [ ] Aggiungere più log.
- [ ] Riorganizzare il codice.
- [ ] Documentare il codice.

## Miglioramenti Utente e Sicurezza

- [ ] Migliorare l'interfaccia utente.
- [ ] Aggiungere misure di sicurezza.
- [ ] Migliorare la gestione dell'input utente:
    - [ ] Implementare una coda per i comandi ricevuti con un buffer limitato e gestione dell'overflow. (?)
    - [ ] Creare un sistema per eliminare i messaggi (risposte del bot e comandi inseriti dall'utente) dopo un certo tempo. (?)

## Miglioramenti Funzionali

- [ ] Implementare la funzionalità "pull" con un comando.
- [ ] Migliorare la ricerca dei file con "find".
- [ ] Cachare i risultati delle query frequenti.

## Gestione di Più Repository

- [ ] Supportare più repository:
    - [ ] Inviare messaggi riguardanti commit da repository multipli.
    - [ ] Comandi per selezionare quali repository controllare.
    - [ ] Comandi per aggiungere e rimuovere repository.

