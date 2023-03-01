# API per la gestione di prodotti e fatture

Lo script e' stato testato su py3.7

**NB.** Inizialmente non ci sara' nessun prodotto e invoice nel database. Se si ha la necessita' di aggiungerli si puo utilizzare il metodo `Database.add_sample_products()` per aggiungere 3 prodotti sample stessa cosa per le invoices con `Database.add_sample_invoices()`

## Requirements
### E' necessario prima installare fastapi 
```bash
python3 -m pip install fastapi
```
### Per avviare lo script
```bash
python3 main_fastapi.py
```

## Documentazione interattiva API
Per vedere una documentazione completa delle api con i relativi endpoint e una pagina interattiva dove testare i vari endpoint della API visitare http://127.0.0.1:8000/docs




## Per avviare unittest
```python
python -m unittest test_api.TestAPI
```
