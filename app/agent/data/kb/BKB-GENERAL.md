# Brambilla Forniture: cosa chiediamo al nuovo CRM

Siamo Brambilla Forniture S.p.A., distributore di forniture industriali in Nord Italia. Dal 2011
lavoriamo su Sinergia 4, un CRM installato in azienda che non viene più aggiornato, e lo
spegniamo. Il vostro CRM è quello su cui lavoreremo da domani: vi diamo l'export completo di
Sinergia del 1° dicembre 2026 e qui sotto quello che ci serve.

I dati li hanno scritti a mano decine di persone in quindici anni: li troverete in molte forme, e
Sinergia aveva abitudini che nessuno ha mai messo per iscritto. Dove una richiesta non dice
qualcosa, guardate i dati: dentro c'è sempre quello che serve per capire cosa devono diventare.

Le richieste sono numerate. In fondo c'è l'allegato con i nomi precisi che usiamo: proprietà,
pipeline, fasi. Quelli vanno rispettati alla lettera, perché li usano i nostri controlli.

## I dati di Sinergia

L'export è un archivio zip con nove file CSV (`sinergia-export/`, separatore `;`, codifica
Windows-1252): aziende, contatti, trattative, righe d'offerta, listino, ticket, attività, utenti e
storico delle fasi delle trattative. Il CRM lo importa da `POST /__migrate` (vedi la consegna).

Valgono per tutti i dati:

- un record marcato come cancellato in Sinergia non si porta, e non conta come doppione di
  nessuno;
- nomi e testi devono arrivare come li hanno scritti le persone, senza spazi di troppo intorno;
- ogni azienda, contatto, trattativa, riga d'offerta, ticket e attività tiene il codice che aveva
  in Sinergia nella proprietà `id_legacy`: il codice della riga di Sinergia da cui viene;
- quando più righe di Sinergia sono lo stesso record, ne resta uno: tiene il codice della riga
  modificata più di recente, e ogni campo prende il valore della riga più recente che lo ha
  compilato;
- un riferimento a un record che non si porta (cancellato o inesistente) è come un campo vuoto,
  anche quando si uniscono i doppioni; il record che lo contiene si porta lo stesso. Un
  riferimento a una riga unita a un'altra va al record che è rimasto.


 i nomi che usiamo

**Proprietà da creare**, tutte di tipo stringa salvo dove scritto:

| Oggetto | Proprietà | Contenuto |
|---|---|---|
| aziende, contatti, trattative, righe d'offerta, ticket, note, chiamate, email, riunioni | `id_legacy` | il codice di Sinergia |
| trattative | `commerciale` | l'email di chi segue la trattativa, da `utenti.csv` (vedi R3) |
| ticket | `assegnatario` | l'email di chi segue il ticket, da `utenti.csv` (vedi R3) |
| note, chiamate, email, riunioni | `autore` | l'email di chi l'ha scritta, da `utenti.csv` |
| aziende | `partita_iva` | undici cifre, a valore unico (`hasUniqueValue`) |
| aziende | `fatturato_2025` | numero |
| aziende | `classe_cliente` | `A`, `B`, `C` o vuota |

**Fasi del rapporto** (`lifecyclestage` dei contatti): Lead è `lead`, Prospect è
`opportunity`, Cliente è `customer`, Ex cliente è `other`.

**Pipeline delle trattative.** Le Vendite di Sinergia sono la pipeline predefinita del CRM
(`default`); una trattativa senza pipeline è nelle Vendite. Le fasi:

| Codice Sinergia | Fase | `dealstage` |
|---|---|---|
| 01 | Contatto | `appointmentscheduled` |
| 02 | Qualifica | `qualifiedtobuy` |
| 03 | Presentazione | `presentationscheduled` |
| 04 | Decisione | `decisionmakerboughtin` |
| 05 | Contratto | `contractsent` |
| 06 | Vinta | `closedwon` |
| 07 | Persa | `closedlost` |

I Rinnovi sono una pipeline di trattative nuova, con etichetta `Rinnovi` e quattro fasi in
quest'ordine: `Da rinnovare` (probabilità 0.2), `In trattativa` (0.6), `Rinnovato` (chiusa,
vinta, 1.0), `Non rinnovato` (chiusa, persa, 0.0).

**Pipeline dei ticket.** Una pipeline di ticket nuova con etichetta `Assistenza` e quattro fasi
in quest'ordine: `Aperto`, `In lavorazione`, `In attesa del cliente` (aperte) e `Chiuso`
(chiusa). Le priorità di Sinergia diventano quelle di HubSpot (`LOW`, `MEDIUM`, `HIGH`,
`URGENT`); senza priorità il ticket non ne ha.

**Tipi di attività.** Le attività diventano note, chiamate, email e riunioni.
