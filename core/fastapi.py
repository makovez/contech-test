from fastapi import FastAPI, Request, Body, Form
from pydantic import BaseModel
from db import Database
from typing import Optional


class InvoiceRequest(BaseModel):
    products: list


app = FastAPI()
db = Database()

@app.post('/addProduct')
def add_product(
    request: Request,
    name: str = Body(...), price: float = Body(...)):
    """
    Aggiunge un nuovo prodotto al database.

    :return: JSON che contiene il messaggio di successo, il nome, il prezzo e l'id del nuovo prodotto.
    """
    # Inserimento di un nuovo prodotto nel database
    product_id = db.add_product(name, price)
    return {'message': 'Prodotto inserito correttamente!', 'name':name, 'price':price, 'id':product_id}


@app.post('/addInvoice')
def add_invoice(
    invoice_request: InvoiceRequest = Body(..., example={"products": [{"product_id": 1, "quantity": 10}, {"product_id": 2, "quantity": 4}]}),
):
    """
    Aggiunge una nuova fattura al database.

    :return: JSON che contiene il messaggio di successo, i prodotti della fattura e l'id della nuova fattura.
    """
    # Inserimento di una nuova fattura nel database
    products = invoice_request.products
    invoice_id = db.add_invoice(products)
    return {'message': 'Fattura inserita correttamente!', 'products':products, 'id':invoice_id}

@app.get('/getProducts')
@app.get('/getProducts/{product_id}')
def get_products(product_id: Optional[int] = None):
    """
    Recupera tutti i prodotti dal database.

    :param product_id: l'id del prodotto da recuperare (opzionale)
    :return: JSON che contiene i prodotti recuperati dal database.
    """
    # Recupero di tutti i prodotti dal database
    products = db.get_products(product_id)
    return products

@app.get('/getInvoices')
@app.get('/getInvoices/{invoice_id}')
def get_invoices(invoice_id: Optional[int] = None):
    """
    Recupera tutte le fatture dal database, con il totale dei prezzi dei prodotti.

    :param invoice_id: l'id della fattura da recuperare (opzionale)
    :return: JSON che contiene le fatture recuperate dal database.
    """
    # Recupero di tutte le fatture dal database, con il totale dei prezzi dei prodotti
    invoices = db.get_invoices(invoice_id)
    return invoices

@app.put('/products/{product_id}')
def update_product(product_id: int, name: str = Body(...), price: float = Body(...)):
    """
    Aggiorna un prodotto nel database.

    :param product_id: l'id del prodotto da aggiornare.
    :return: JSON che contiene il messaggio di successo, il nome e il prezzo del prodotto aggiornato.
    """
    db.update_product(product_id, name, price)
    return {'message': 'Product updated successfully', 'name':name, 'price':price, 'id':product_id}

@app.put('/invoices/{invoice_id}')
def update_invoice(invoice_id: int, 
                   invoice_request: InvoiceRequest = Body(..., example={"products": [{"product_id": 1, "quantity": 10}, {"product_id": 2, "quantity": 4}]})):
    """
    Aggiorna una fattura nel database.

    :param invoice_id: l'id della fattura da aggiornare.
    :return: JSON che contiene il messaggio di successo, i prodotti della fattura aggiornata e l'id della fattura.
    """
    products = invoice_request.products
    db.update_invoice(invoice_id, products)
    return {'message': 'Invoice updated successfully', 'products':products, 'id':invoice_id}
