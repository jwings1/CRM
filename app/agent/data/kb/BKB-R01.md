# R1. Le aziende
Le aziende diventano `companies`, con ragione sociale (`name`), sito (`domain`: solo il
dominio), città (`city`) e sigla della provincia (`state`). Un'azienda deve esistere una volta
sola: per esempio, due schede con lo stesso sito sono la stessa azienda. Quando più schede sono la
stessa azienda e si uniscono, l'azienda che resta tiene anche i siti delle altre schede (in
HubSpot, `hs_additional_domains`).
