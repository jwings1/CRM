# R8. Il fatturato 2025 e la classe del cliente
Ogni azienda ha il fatturato vinto nel 2025 in `fatturato_2025` (euro, due decimali, `0` se non
ce n'è) e la sua classe in `classe_cliente`.

- Il fatturato è quello che resta davvero nel 2025: le trattative vinte (Vinta nelle vendite,
  Rinnovato nei rinnovi) con data di chiusura nel 2025 e associate all'azienda, tolto quello che
  nello stesso anno abbiamo stornato a quell'azienda.
- Le trattative in dollari e sterline si convertono in euro ai cambi fissi del nostro
  controllo di gestione: 1 USD = 0,92 EUR, 1 GBP = 1,17 EUR. Si somma tutto e si arrotonda il
  totale al centesimo.
- La classe è `A` da 100.000 euro in su, `B` da 20.000, `C` sopra zero; con un fatturato di zero
  o negativo la classe resta vuota.

Si calcolano sui dati importati da Sinergia: ci servono il giorno dopo la migrazione.
