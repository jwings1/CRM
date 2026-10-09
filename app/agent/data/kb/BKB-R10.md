# R10. Trattativa vinta, si apre l'avvio fornitura
Quando una trattativa entra nella fase Vinta della pipeline delle vendite, perché ci viene
spostata o perché viene creata direttamente lì, il CRM apre un ticket
nella pipeline `Assistenza`, fase `Aperto`, con oggetto `Avvio fornitura - ` seguito dal titolo
della trattativa, `assegnatario` uguale al `commerciale` della trattativa, associato alla
trattativa e alle sue aziende. Una volta sola per trattativa, anche se torna indietro e poi di
nuovo a Vinta.
