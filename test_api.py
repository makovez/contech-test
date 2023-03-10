import unittest
import json, time
from fastapi.testclient import TestClient
from core.fastapi import app
from db import Database

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.db = Database()
        self.db.flush_tables()
        # Qua bisognerebbe inializzare un nuovo db con dei prodotti samples e poi testare
        # che tutti i metodi funzionano correttamente

    def test_get_products(self):
        # Aggiungo prodotti samples
        self.db.add_sample_products()

        # Ottengo tutti i prodotti
        response = self.client.get('/getProducts')

        # Controllo che ci siano tutti i prodotti
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)  # Supponendo che ci siano tre prodotti nella tabella

    def test_get_invoices(self):
        # Aggiungo fattura sample
        self.db.add_sample_invoices()

        # Ottengo tutte le fatture
        response = self.client.get('/getInvoices')

        # Controllo che la risposta sia corrette e il numero di fatture corrisponde
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)  # Supponendo che ci sia almeno una fattura nella tabella

    def test_add_invoice(self):
        response = self.client.post('/addInvoice', json={"products": [{"product_id": 1, "quantity": 2}, {"product_id": 2, "quantity": 3}]})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.json()['id'], 0)

    def test_add_product(self):
        response = self.client.post('/addProduct', json={"name": "Prodotto test", "price": 10.0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], "Prodotto test")
        self.assertEqual(response.json()['price'], 10.0)

    def test_update_product(self):
        # Aggiungo un nuovo prodotto
        response = self.client.post('/addProduct', json={"name": "Prodotto test", "price": 10.0})
        product_id = response.json()['id']
        # Modifico il prodotto
        response = self.client.put(f'/products/{product_id}', json={"name": "Prodotto test modificato", "price": 12.0})

        # Controllo che la risposta sia corretta
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], "Prodotto test modificato")
        self.assertEqual(response.json()['price'], 12.0)

    def test_update_invoice(self):
        # Aggiungo una nuova fattura
        response = self.client.post('/addInvoice', json={"products": [{"product_id": 1, "quantity": 2}, {"product_id": 2, "quantity": 3}]})
        invoice_id = response.json()['id']
        # Modifico la fattura
        response = self.client.put(f'/invoices/{invoice_id}', json={"products": [{"product_id": 1, "quantity": 5}, {"product_id": 2, "quantity": 1}, {"product_id": 3, "quantity": 4}]})
        # Controllo che la risposta sia corretta
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['products'], [{"product_id": 1, "quantity": 5}, {"product_id": 2, "quantity": 1}, {"product_id": 3, "quantity": 4}])
        
    
    
    