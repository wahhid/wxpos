import pos

import pos.modules.base.objects.common as common

import pos.modules.currency.objects.currency as currency

import pos.modules.stock.objects.category as category

class Product(common.Item):
    data_keys = ('name', 'description', 'reference', 'code',
                 'price', 'currency', 'quantity', 'category',
                 'in_stock')
    
    def getData(self):
        sql = "SELECT name, description, reference, code,"+\
                        " price, currency_id, quantity, category_id"+\
                " FROM products WHERE id=%s AND state>0"
        params = (self.id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                self.data['name'], self.data['description'], \
                    self.data['reference'], self.data['code'], \
                    self.data['price'], currency_id, \
                    self.data['quantity'], category_id = results
                self.data['in_stock'] = self.data['quantity'] is not None
                if category_id is not None:
                    self.data['category'] = category.find(_id=category_id)
                else:
                    self.data['category'] = None
                self.data['currency'] = currency.find(_id=currency_id)

    def updateQuantity(self, quantity, operation):
        sql = "INSERT INTO stockdiary (operation, quantity, product_id, date)"+\
              " VALUES (%s, %s, %s, NOW())"
        params = (operation, quantity, self.id)
        cursor, success = pos.db.query(sql, params)
        if not success:
            return None
        
        if operation == 'in':
            return self.update(quantity=self.data['quantity']+quantity)
        elif operation == 'out':
            return self.update(quantity=self.data['quantity']-quantity)
        else:
            return self.update(quantity=quantity)

class ProductObject(common.Object):
    item = Product
    def dbGetAll(self):
        sql = "SELECT id FROM products WHERE state>0"
        params = None
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None
    
    def dbInsert(self, name, description, reference, code,
             price, currency_id, quantity, category_id, in_stock):
        sql = """INSERT INTO products
            (name, description, reference, code,
             price, currency_id, quantity, category_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""
        params = (name, description, reference, code,
                  price, currency_id, quantity if in_stock else None, category_id)
        cursor, success = pos.db.query(sql, params)
        if success:
            _id = pos.db.conn.insert_id()
            return _id
        else:
            return None

    def dbUpdate(self, _id, **kwargs):
        if kwargs.has_key('in_stock') and kwargs['in_stock']:
            kwargs['quantity'] = None
        fields = ('name', 'description', 'reference', 'code', 'price', 'currency_id', 'quantity', 'category_id')
        update_str = ",".join([f+"=%s" for f in fields if kwargs.has_key(f)])
        update_params = [kwargs[f] for f in fields if kwargs.has_key(f)]
        
        if len(update_str) == 0: return True
        sql = "UPDATE products SET "+update_str+" WHERE id=%s"
        params = update_params+[_id]
        cursor, success = pos.db.query(sql, params)
        if success:
            return True
        else:
            return None
    
    def dbDelete(self, _id):
        sql = "UPDATE products SET state=-1 WHERE id=%s"
        params = (_id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def getDBData(self, key, val):
        if key == 'category':
            if val is None:
                return 'category_id', None
            else:
                return 'category_id', val.id
        elif key == 'currency':
            return 'currency_id', val.id
        else:
            return key, val

obj = ProductObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
add = lambda **kwargs: obj.add(**kwargs)
