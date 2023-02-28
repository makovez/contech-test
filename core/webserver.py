from flask import Flask, request, jsonify
from db import Database

db = Database()
app = Flask(__name__)

@app.route('/addProduct', methods=['POST'])
def addProduct():
    """
    Aggiunge un nuovo prodotto al database.

    :return: JSON che contiene il messaggio di successo, il nome, il prezzo e l'id del nuovo prodotto.
    """
    # Inserimento di un nuovo prodotto nel database
    data = request.get_json()
    name, price = data['name'], data['price']
    product_id = db.add_product(name, price)
    return jsonify({'message': 'Prodotto inserito correttamente!', 'name':name, 'price':price, 'id':product_id})


@app.route('/addInvoice', methods=['POST'])
def addInvoice():
    """
    Aggiunge una nuova fattura al database.

    :return: JSON che contiene il messaggio di successo, i prodotti della fattura e l'id della nuova fattura.
    """
    # Inserimento di una nuova fattura nel database
    data = request.get_json()
    products = data['products']
    invoice_id = db.add_invoice(products)
    return jsonify({'message': 'Fattura inserita correttamente!', 'products':products, 'id':invoice_id})

@app.route('/getProducts', methods=['GET'])
@app.route('/getProducts/<int:product_id>', methods=['GET'])
def getProducts(product_id = None):
    """
    Recupera tutti i prodotti dal database.

    :param product_id: l'id del prodotto da recuperare (opzionale)
    :return: JSON che contiene i prodotti recuperati dal database.
    """
    # Recupero di tutti i prodotti dal database
    products = db.get_products(product_id)
    return jsonify(products)

@app.route('/getInvoices', methods=['GET'])
@app.route('/getInvoices/<int:invoice_id>', methods=['GET'])
def getInvoices(invoice_id = None):
    """
    Recupera tutte le fatture dal database, con il totale dei prezzi dei prodotti.

    :param invoice_id: l'id della fattura da recuperare (opzionale)
    :return: JSON che contiene le fatture recuperate dal database.
    """
    # Recupero di tutte le fatture dal database, con il totale dei prezzi dei prodotti
    invoices = db.get_invoices(invoice_id)
    return jsonify(invoices)

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Aggiorna un prodotto nel database.

    :param product_id: l'id del prodotto da aggiornare.
    :return: JSON che contiene il messaggio di successo, il nome e il prezzo del prodotto aggiornato.
    """
    data = request.get_json()
    db.update_product(product_id, data)
    return jsonify({'message': 'Product updated successfully', 'name':data['name'], 'price':data['price']})

@app.route('/invoices/<int:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    """
    Aggiorna una fattura nel database.

    :param invoice_id: l'id della fattura da aggiornare.
    :return: JSON che contiene il messaggio di successo e i prodotti della fattura aggiornata.
    """
    data = request.get_json()
    products = data['products']
    db.update_invoice(invoice_id, products)
    return jsonify({'message': 'Invoice updated successfully', 'products':products})