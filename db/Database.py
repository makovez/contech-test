import sqlite3

class Database:
    def __init__(self, file_name = 'invoices.db') -> None:
        # Connessione al database SQLite
        self.conn = sqlite3.connect(file_name, check_same_thread=False)
        self.c = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def initialize_db(self):
        # Inizializza il database creando le tabelle e aggiungendo alcuni prodotti di esempio
        self.create_tables()
        self.add_sample_products()
        self.commit()

    def create_tables(self):
        # Creazione della tabella 'products'
        self.c.execute('''CREATE TABLE IF NOT EXISTS products
                    (id INTEGER PRIMARY KEY, name TEXT, price INTEGER)''')

        # Creazione della tabella 'invoices'
        self.c.execute('''CREATE TABLE IF NOT EXISTS invoices
                  (id INTEGER PRIMARY KEY,
                   date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        # Creazione della tabella di join 'invoice_products'
        self.c.execute('''CREATE TABLE IF NOT EXISTS invoice_products
                    (invoice_id INTEGER, product_id INTEGER, quantity INTEGER,
                    FOREIGN KEY (invoice_id) REFERENCES invoices(id),
                    FOREIGN KEY (product_id) REFERENCES products(id))''')
        
    def add_sample_products(self):   
        # Inserimento di alcuni dati di esempio nel database
        self.c.execute("INSERT INTO products (name, price) VALUES ('Prodotto 1', 10.0)")
        self.c.execute("INSERT INTO products (name, price) VALUES ('Prodotto 2', 15.0)")
        self.c.execute("INSERT INTO products (name, price) VALUES ('Prodotto 3', 20.0)")

    def execute_safe_query(self, query, params=None, include_params=False):
        if include_params:
            self.c.execute(query, params)
        else:
            self.c.execute(query)


    def add_product(self, name, price):
        """
        Aggiunge un nuovo prodotto al database con il nome e prezzo specificati.
        
        :param name: Il nome del prodotto da aggiungere.
        :param price: Il prezzo del prodotto da aggiungere.
        :return: L'ID del nuovo prodotto aggiunto al database.
        """
        # Aggiunge un prodotto al database
        self.c.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        self.commit()
        product_id = self.c.lastrowid
        return product_id

    def add_invoice(self, products):
        """
        Aggiunge una nuova fattura al database contenente i prodotti specificati.
        
        :param products: Una lista di dizionari contenente i dettagli dei prodotti aggiunti alla fattura.
                        Ogni dizionario deve contenere 'product_id' e 'quantity'.
        :return: L'ID della nuova fattura aggiunta al database.
        """
        # Recupera tutti i prodotti dal database
        self.c.execute("INSERT INTO invoices DEFAULT VALUES")
        invoice_id = self.c.lastrowid
        for item in products:
            product_id = item['product_id']
            quantity = item['quantity']
            self.c.execute("INSERT INTO invoice_products (invoice_id, product_id, quantity) VALUES (?, ?, ?)",
                      (invoice_id, product_id, quantity))
        self.commit()
        return invoice_id

    def get_products(self, product_id = None):
        """
        Restituisce una lista di dizionari contenente le informazioni sui prodotti presenti nel database. Se product_id e' specificato, soltanto questo prodotto verra' preso in considerazione.
        
        :param product_id: (opzionale) l'ID del prodotto da cercare. Se non specificato, verranno restituiti tutti i prodotti.
        :return: una lista di dizionari contenente le informazioni sui prodotti, con le seguenti chiavi: 'id', 'name', 'price'
        """
        # Recupero di tutti i prodotti dal database
        self.execute_safe_query(
            "SELECT * FROM products "
            "{0}".format('WHERE id = ?' if product_id else ''),
            params=(product_id,), include_params=bool(product_id))
        
        products = self.c.fetchall()

        # Aggiungo le chiavi ai prodotti
        result = []
        for product in products:
            result.append({'id': product[0], 'name': product[1], 'price': product[2]})

        return result
    
    def update_product(self, product_id, data):
        """
        Update a product in the database with the given product_id and data.
        :param product_id: The id of the product to update.
        :param data: A dictionary containing the updated data for the product.
                    The dictionary can contain the keys 'name' and/or 'price'.
        """
        # Update product fields in the database based on the provided data
        set_clause = ", ".join([f"{key}=? " for key in data.keys()])
        values = tuple(data.values()) + (product_id,)
        self.c.execute(f"UPDATE products SET {set_clause} WHERE id=?", values)
        self.conn.commit()


    def update_invoice(self, invoice_id, products):
        """
        Aggiorna una fattura esistente nel database. Cancella tutti i record di invoice_products associati alla fattura specificata e inserisce i nuovi record specificati nella lista di prodotti.

        :param invoice_id: l'id della fattura da aggiornare
        :param products: una lista di dizionari contenenti i dettagli dei prodotti da aggiungere alla fattura
        :return: None
        """
        # Cancella tutti i record di invoice_products per questa fattura
        self.c.execute("DELETE FROM invoice_products WHERE invoice_id = ?", (invoice_id,))
        
        # Inserisci i nuovi record di invoice_products per questa fattura
        for product in products:
            product_id = product['product_id']
            quantity = product['quantity']
            self.c.execute("INSERT INTO invoice_products (invoice_id, product_id, quantity) VALUES (?, ?, ?)",
                      (invoice_id, product_id, quantity))
        
        self.commit()
        
        
    
    def get_invoices(self, invoice_id = None):
        """
        Restituisce una lista di dizionari rappresentanti le fatture presenti nel database.
        Ogni dizionario contiene le seguenti informazioni:
            - id: l'ID della fattura
            - date: la data della fattura
            - total: il totale della fattura (calcolato come la somma del prezzo dei prodotti moltiplicato per la loro quantità)
            - products: una lista di dizionari contenenti le informazioni sui prodotti presenti nella fattura. 
            Ogni dizionario contiene le seguenti informazioni:
                - name: il nome del prodotto
                - quantity: la quantità del prodotto presente nella fattura
                - price: il prezzo del prodotto
                - subtotal: il subtotale del prodotto (calcolato come il prodotto tra il prezzo e la quantità)

        Se viene specificato un valore per il parametro invoice_id, il metodo restituisce solo le fatture corrispondenti a quell'ID.
        In caso contrario, il metodo restituisce tutte le fatture presenti nel database.

        :param invoice_id: l'ID della fattura da cercare (opzionale)
        :return: la lista di dizionari contenenti le informazioni sulle fatture
        """
        self.execute_safe_query("SELECT invoices.id, invoices.date, SUM(products.price * invoice_products.quantity) as total, products.name, invoice_products.quantity, products.price, "
                        "invoice_products.quantity * products.price as subtotal "
                        "FROM invoices "
                        "JOIN invoice_products ON invoices.id = invoice_products.invoice_id "
                        "JOIN products ON invoice_products.product_id = products.id "
                        "{0} "
                        "ORDER BY invoices.id, products.name".format("WHERE invoice_id = ?" if invoice_id else ''),
                        params=(invoice_id,), include_params=bool(invoice_id))
        rows = self.c.fetchall()
        invoices = []
        for invoice_id, date, total, *products_data in rows:
            if not invoices or invoices[-1]['id'] != invoice_id:
                invoices.append({'id': invoice_id, 'date': date, 'products': [], 'total':total})
            product = dict(zip(('name', 'quantity', 'price', 'subtotal'), products_data))
            invoices[-1]['products'].append(product)

        return invoices
