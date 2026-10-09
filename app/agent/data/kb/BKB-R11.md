# R11. Trattativa persa, si richiama tra sei mesi
Quando una trattativa entra nella fase Persa della pipeline delle vendite, spostata o creata
lì, il CRM crea un task
associato alla trattativa, con oggetto (`hs_task_subject`) `Richiamare: ` seguito dal titolo
della trattativa, scadenza (`hs_timestamp`) 180 giorni dopo l'ingresso in Persa, stato
(`hs_task_status`) `NOT_STARTED`. Una volta sola per trattativa.
