# R7. La partita IVA
Ogni azienda ha la sua partita IVA nella proprietà `partita_iva`, quando la conosciamo: undici
cifre, senza `IT` e senza spazi. Non devono più esistere due aziende con la stessa partita IVA:
`partita_iva` è una proprietà a valore unico, e il CRM rifiuta di creare un'azienda con una
partita IVA che c'è già, rispondendo `409`.
