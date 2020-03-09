# Animal'sCare

## Progetto Applicazioni web e mobile – Berselli Werther, Di Blasi Fabrizio
Applicazione web e mobile per la gestione di annunci di pet sitting.

### Applicazione web (Django)
L'applicazione è utilizzabile sia da utenti anonimi che da utenti registrati:
- Gli utenti anonimi possono vedere gli annunci dei pet sitter in base alla categoria scelta (cani, gatti ecc.), o di chi cerca un pet sitter per il proprio animale; può inoltre vedere i profili degli utenti registrati e le eventuali recensioni che essi hanno ricevuto (nel caso di profili di pet sitter).
- Gli utenti registrati possono prenotare un pet sitter (o inserire un annuncio) e in seguito inserire un voto e una recensione.
-Gli annunci comprendono una data di inizio e una data di fine, un titolo, un logo e una descrizione. Possono essere modificati o eliminati dall’inserzionista in qualsiasi momento.
- I pet sitter possono rispondere a un annuncio di un utente o inserirne uno nuovo (e viceversa); tutti gli utenti possono consultare una sezione privata “Calendario” e vedere i loro prossimi impegni e il loro “storico” degli impegni passati.
- L’inserzionista (utente o pet sitter) riceve una mail quando qualcuno ha risposto al suo annuncio.
- Le prestazioni di pet sitting possono essere pagate tramite accordo fra utente e pet sitter (accordo esterno all’applicazione) o tramite l’uso dei “Pet Coins”. I Pet Coins possono essere “acquistati” (simulato nell’applicazione) dagli utenti, e trasferiti al pet sitter che potrà riscattarli in denaro a fronte di una piccola trattenuta del sito.
-  L’applicazione gestisce le prenotazioni per cani, gatti e altri animali; vengono incluse possibili passeggiate (con i cani), ore di compagnia, oppure nel caso di pesci e uccelli la gestione di acqua, cibo ed eventuale pulizia di acquari o gabbie. Possibilità di annunci per accompagnare l’animale dal veterinario in caso di bisogno se il padrone è impossibilitato.
- Possibilità di vedere una classifica dei migliori pet sitter, ordinati per voto o per numero di recensioni positive ricevute; possibilità di vedere i pet sitter più vicini con l’integrazione di Google Maps.
- Creazione di un profilo per utenti e pet sitter con dati, descrizione e una foto; possibilità di modificare o eliminare il proprio profilo utente.
- Possibilità di contattare gli admin per domande e suggerimenti mediante un’apposita sezione.
- Possibilità di utilizzare Google Oauth per accedere al sito.
- Tutte le form saranno validate in tempo reale con Ajax e Jquery.
- Unit test su tutte le applicazioni.

### Applicazione Mobile
- Realizzazione di un'app mobile con React Native per poter fruire nativamente delle funzionalità del sito su dispositivi mobili.
