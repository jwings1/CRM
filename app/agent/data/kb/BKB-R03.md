# R3. Le trattative
Le trattative diventano `deals`, con titolo, importo (`amount`, il numero) e valuta
(`deal_currency_code`: `EUR`, `USD` o `GBP`; senza indicazioni è euro), pipeline e fase (vedi
l'allegato), data di chiusura (`closedate`), il commerciale che la segue (`commerciale`) e le
associazioni all'azienda e ai contatti, ognuno una volta sola. Una trattativa senza importo non
ha né importo né valuta.

- Una trattativa con righe d'offerta vale il totale delle sue righe.
- I rinnovi sono annuali.
- Le trattative e i ticket li segue chi lavora oggi da noi: chi ha lasciato l'azienda non segue
  più niente.
