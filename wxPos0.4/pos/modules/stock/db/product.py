class ProductDB:
    def getAllProducts(self):
        sql = "SELECT id FROM products WHERE state>0"
        params = None
        cursor, success = self.db.query('getAllProducts', sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None

    def insertProduct(self, name, description, reference, code,
             price, currency_id, quantity, category_id):
        sql = """INSERT INTO products
            (name, description, reference, code,
             price, currency_id, quantity, category_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""
        params = (name, description, reference, code,
                  price, currency_id, quantity, category_id)
        cursor, success = self.db.query('insertProduct', sql, params)
        if success:
            product_id = self.conn.insert_id()
            return product_id
        else:
            return None

    def updateProduct(self, product_id, name=None, description=None,
                      reference=None, code=None, price=None,
                      currency_id=None, quantity=None, category_id=None):
        fields = ('name', 'description', 'reference', 'code', 'price', 'currency_id', 'quantity', 'category_id')
        update_str = [f+"=%s" for f in fields if locals()[f] is not None]
        if len(update_str) == 0: return None
        
        sql = "UPDATE products SET "+",".join(update_str)+" WHERE id=%s AND state>0"
        params = [locals()[f] for f in fields if locals()[f] is not None]
        params.append(product_id)
        cursor, success = self.db.query('updateProduct', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def deleteProduct(self, product_id):
        sql = "UPDATE products SET state=-1 WHERE id=%s"
        params = (product_id,)
        cursor, success = self.db.query('deleteProduct', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None
    
    def getProductInfo(self, product_id):
        sql = """SELECT name, description, reference, code,
                        price, currency_id, quantity, category_id
                FROM products WHERE id=%s AND state>0
"""
        params = (product_id,)
        cursor, success = self.db.query('getProductInfo', sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                return results
            else:
                return None
        else:
            return None
