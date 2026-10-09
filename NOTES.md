# NOTES — data cases found (feeds the choice sheet at 15:00)

Counts are from the export we got (`legacy/export.zip`). Code: `app/migrate/normalize.py` (parsers), `app/migrate/transform.py` (rules).
Migration time: ~31 s locally end-to-end (read 3 s, transform 8 s, load 17 s).

## Case: deleted flag written 9 ways
- **Where**: `cancellato` in every file
- **Example**: kept `''`, `0`, `N`, `NO`; deleted `S`, `s`, `SI`, `Sì`, `1`
- **Rows**: deleted aziende 799, contatti 2,802, opportunita 1,443, attivita 10,713, listino 70
- **Rule**: deleted = one of S/SI/Sì/1 (case-insensitive). Deleted rows are dropped before any merge; references to them = empty field.

## Case: duplicate companies (same website OR same VAT number)
- **Where**: `aziende.sito_web`, `aziende.note`
- **Example**: `281866;Nuova Cablaggi Negri;www.nuovacablagginegri.it` + `18098;Nuova Cablaggi Negri S.p.A.;https://nuovacablagginegri.it;P. IVA: IT 87397933331`
- **Rows**: 1,964 rows merged into 1,722 companies (17,734 left). 381 VAT groups have different domains (`dellavalleautomazione.eu` / `DELLAVALLEAUTOMAZIONEGROUP.IT`).
- **Rule**: union-find on normalized domain (lowercase, no scheme, no `www.`, no path) and on VAT number. Survivor = most recent `ultima_modifica` (keeps its `id_legacy`); every field = most recent non-empty; other domains → `hs_additional_domains`.
- **Ruled out**: merging by name only (2,689 shared folded names, many are different companies in different cities).

## Case: VAT number lives in the notes
- **Where**: `aziende.note`
- **Example**: `partita iva 84874 281912`, `P. IVA: IT 40969350707`, `p.iva IT11476373136`, `P.IVA 67105837370`
- **Rows**: 8,263, all 11 digits after cleanup
- **Rule**: regex on `p.iva|partita iva`, drop `IT` and spaces. Loaded into `unique_values` so R7 409 works on migrated data; the write path normalizes `IT 123…` too.

## Case: duplicate contacts, including obfuscated emails
- **Where**: `contatti.email`
- **Example**: `alessia.vitale(at)gmail.com`, `beatrice.testa @libero.it`, `ROBERTOPOZZI@X.IT `
- **Rows**: 6,376 rows merged into 5,341 people. 936 repairable emails, 180 of which equal another contact's valid email (proof they're duplicates). 3,532 invalid → no email (`n.d.`, `da chiedere`, `-`, `nessuna`, `NO EMAIL`, `x@gmail`).
- **Rule**: repair `(at)`→`@`, drop spaces around `@`, lowercase; valid = strict regex. Merge by email; survivor/fields as for companies. Company reference = most recent row whose reference is valid.
- **Ruled out**: merging email-less contacts by name+company (737 groups; too risky without a key).

## Case: contacts without a company (R12 on history)
- **Rows**: 13,022 empty + 1,754 pointing to non-existent ids (9 digits) + 1,881 to deleted companies → 2,955 associated via email domain
- **Rule**: domain of the email = a company's domain or additional domain → contact→company (primary). Never creates companies.

## Case: deal amounts in mixed formats
- **Where**: `opportunita.importo`, `valuta`
- **Example**: `€ -5.131,24`, `€24,376.08`, `EUR 223.370,86`, `€ 1027956.14`, `(20020,40)`, `€206,5k`, `6.5mila`, `1,2 mln`, `51.315,91 mensili`, `€ 77.505,65/mese`
- **Rule**: both separators → the last is decimal; one separator repeated or followed by exactly 3 digits → thousands; else decimal. `k`/`mila` ×1,000, `mln` ×1,000,000. `(…)` or `-` → negative. Currency from the symbol/code in the amount, else `valuta`, else EUR. No amount → no amount and no currency.

## Case: monthly renewals ("I rinnovi sono annuali")
- **Rows**: 810 deals, all in the Rinnovi pipeline (`mensili`, `/mese`, `al mese`)
- **Rule**: amount ×12.

## Case: refunds (storni / credit notes)
- **Example**: `Storno fattura 5079/2018 - Officine Sironi;… € -5.131,24;…;06`, `Nota di credito n. 363/2016`, `NC 615/24`, `(20020,40)`
- **Rows**: 945 negative-amount deals in a won stage, 35 in other stages
- **Rule**: kept as deals with negative `amount`. R8 sums won deals closed in 2025 including the negatives (= revenue minus refunds of the year). R9 "has a won deal" counts only positive won deals.

## Case: close date missing or odd
- **Where**: `opportunita.data_chiusura`, `storico_fasi`
- **Example**: `''`, `42466` (Excel serial), `12.03.19`, `20-04-2017`, `9/3/2015`, `16/03/2014 00:00:00`
- **Rows**: 11,341 empty; 2,656 closed deals recovered from `storico_fasi` (date of the last move into the current closed stage; where both exist they always agree)
- **Rule**: all formats parsed; closedate stored as the calendar day at 00:00Z.

## Case: stage and pipeline spellings
- **Example**: `06`, `06 VINTA`, `06 - Vinta`, ` vinta`, `R3 - Rinnovato`, `r2`, `IN TRATTATIVA`; pipeline `vendite `, `RINNOVI`, `''`
- **Rule**: stage parsed by code or keyword; the stage family decides the pipeline; empty pipeline = Vendite.

## Case: deal owner written as a name; owners who left
- **Where**: `opportunita.id_commerciale`, `ticket.id_utente`, `utenti.attivo/responsabile`
- **Example**: `francesca marchetti`, `Mazza E.`, `T. Lombardo`, `D'AMICO NICCOLÒ`; `U05 … attivo=n, responsabile=U01`
- **Rows**: 156 free-text owners (all resolved); 20 inactive users
- **Rule**: match name/surname/initial (accent-insensitive). Inactive owner → their `responsabile`, up the chain to the first active one ("li segue chi lavora oggi da noi"). Activity `autore` stays the real author.

## Case: quote lines
- **Example**: qty `2,5 m`, `10 pz`; price `€ 1.151,12`, empty; discount `15%`, `15,0`, `0,15`; SKU `bf38295`, `art. 38295`, `BF.3829`
- **Rows**: 2,640 lines without a price; discount fractions ~3,000 (`0,25` `0,15` `0,1` `0,05` `0,03` mirror 25/15/10/5/3 %); 1,722 lines of deleted deals dropped
- **Rule**: price empty → list price valid at the deal date (price-list version with the latest `ultima_modifica` ≤ deal date). Discount < 1 without `%` → ×100. Line total = qty × price × (1 − disc), rounded to the cent; deal amount = sum of its lines (EUR).

## Case: price list republished
- **Rows**: 1,922 rows → 1,735 products (SKUs `BF38295` and `BF-38295` are the same article)
- **Rule**: SKU normalized to `BF-01234`; name and price from the latest version.

## Case: tickets
- **Example**: stato `RISOLTO`, `Nuovo`, `Lavorazione`, `Attesa cliente`; priorità `2 - Media`, `Normale`, `4 - Urgente`; descrizione `Da: m.leone@cortimetalli.com …`
- **Rule**: RISOLTO/CHIUSO → Chiuso, Nuovo → Aperto, etc.; Normale = MEDIUM; empty priority = none. Missing contact → contact whose email is in `Da:` (456 tickets).

## Case: activity types
- **Example**: `NOTA`, `Appunto` → note; `Telefonata`, `Tel.` → call; `E-mail`, `Mail` → email; `Incontro`, `Riunione`, `Visita`, `Meeting` → meeting

## R8 / R9 results on our export
- R8: 142 companies with 2025 revenue (A 52, B 25, C 65); FX USD 0.92, GBP 1.17; total rounded once.
- R9: 4,123 companies with a won deal; 803 dormant (no activity in 2025 on their contacts or deals). Static list `Clienti dormienti`.

## Legacy audit inside /__migrate (app/audit)
- Rules run on the raw export before transform: 31 anomaly classes, ~96k findings on the starter export, recorded in Postgres schema `audit` (`audit.findings`, `audit.runs`).
- gpt-6-luna judges only cases that change data: 1,433 same-name+city company groups, 161 tickets closed before opened (107 batches, ~$0.045). Merges with confidence >= 0.9 are applied (17 groups / 20 rows on the starter export). Ticket dates: the model can't tell which date is wrong -> left as is.
- The LLM step gets the time left in the 5-min window (250 s budget - elapsed - 90 s reserve, max 180 s); late batches are dropped, never block the migration.
- Fixes found by diffing the audit against transform(): broken accents (~4,200 rows), owner from stage history (656 deals), ticket sender anywhere in text (+400), '1.4mln' (12 deals), latest list price for missing unit prices (93 deals: matches Sinergia's stored amounts on all 11,659 deals with lines).
