# Per avviare unittest
python -m unittest test_api.TestAPI


NB. Inizialmente non ci sara' nessun prodotto e invoice nel database. Se si ha la necessita' di aggiungerli si puo utilizzare il metodo Database.add_sample_products() per aggiungere 3 prodotti sample

# API per la gestione di prodotti e fatture

## Aggiunta di un nuovo prodotto
URL: /addProduct
Metodo HTTP: POST

Input: Il metodo richiede l'invio di un JSON contenente i seguenti campi:

- name: il nome del prodotto (stringa)
- price: il prezzo del prodotto (numero)

Output: Il metodo restituisce un JSON contenente i seguenti campi:

- message: un messaggio di conferma che indica che il prodotto è stato inserito correttamente (stringa)
- name: il nome del prodotto inserito (stringa)
- price: il prezzo del prodotto inserito (numero)
- id: l'ID del prodotto inserito nel database (numero intero)


