# R4. Listino e offerte
Il listino diventa `products`: codice (`hs_sku`, nella forma `BF-01234`), descrizione (`name`) e
prezzo in euro (`price`). Due righe del listino con lo stesso codice sono lo stesso articolo,
ripubblicato a un prezzo nuovo.

Le righe d'offerta diventano `line_items`, associate alla loro trattativa e al prodotto del
listino: descrizione (`name`; se manca, quella dell'articolo), quantità (`quantity`), prezzo
unitario in euro (`price`) e sconto in percentuale (`hs_discount_percentage`, `0` se non c'è). Il
totale di una riga è quantità per prezzo, meno lo sconto, arrotondato al centesimo. Le righe di
una trattativa che non si porta non si portano.
