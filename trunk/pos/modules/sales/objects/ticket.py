import pos

import pos.modules.base.objects.common as common

import pos.modules.currency.objects.currency as currency

import pos.modules.user.objects.user as user

import pos.modules.customer.objects.customer as customer

class Ticket(common.Item):
    data_keys = ('user', 'closed', 'currency', 'customer')
    
    def getData(self):
        sql = "SELECT comment, currency_id, user_id, customer_id, date_close FROM tickets WHERE id=%s"
        params = (self.id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                self.data['comment'], currency_id, user_id, customer_id, self.data['date_close'] = results
                if currency_id is None:
                    self.data['currency'] = None
                else:
                    self.data['currency'] = currency.find(_id=currency_id)
                self.data['user'] = user.find(_id=user_id)
                if customer_id is None:
                    self.data['customer'] = None
                else:
                    self.data['customer'] = customer.find(_id=customer_id)
        
        sql = "SELECT (date_close IS NOT NULL) as 'closed' FROM tickets WHERE id=%s"
        params = (self.id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                self.data['closed'] = bool(results[0])

    def close(self):
        import pos.modules.sales.objects.ticketline as ticketline
        sql = "UPDATE tickets SET date_close=NOW() WHERE id=%s"
        params = (self.id,)
        cursor, success = pos.db.query(sql, params)
        if success and cursor.rowcount == 1:
            self.obj.getAll(refresh=True)
            tls = ticketline.find(list=True, ticket=self)
            for tl in tls:
                p = tl.data['product']
                if p is None or not p.data['in_stock']:
                    continue
                p.updateQuantity(tl.data['amount'], 'out')
        else:
            return None

class TicketObject(common.Object):
    item = Ticket
    def dbGetAll(self):
        sql = "SELECT id FROM tickets WHERE state>0"
        params = None
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None
    
    def dbInsert(self, currency_id, user_id):
        sql = "INSERT INTO tickets (date_open, currency_id, user_id) VALUES (NOW(), %s, %s)"
        params = (currency_id, user_id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            _id = pos.db.conn.insert_id()
            return _id
        else:
            return None
    
    def dbUpdate(self, _id, **kwargs):
        fields = ('comment', 'customer_id')
        update_str = ",".join([f+"=%s" for f in fields if kwargs.has_key(f)])
        update_params = [kwargs[f] for f in fields if kwargs.has_key(f)]
        
        if len(update_str) == 0: return True
        sql = "UPDATE tickets SET "+update_str+" WHERE id=%s"
        params = update_params+[_id]
        cursor, success = pos.db.query(sql, params)
        if success:
            return True
        else:
            return None
    
    def dbDelete(self, _id):
        sql = "UPDATE tickets SET state=-1 WHERE id=%s"
        params = (_id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def getDBData(self, key, val):
        if key == 'user':
            return 'user_id', val.id
        elif key == 'customer':
            return 'customer_id', val.id
        elif key == 'currency':
            return 'currency_id', val.id
        else:
            return key, val

obj = TicketObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
add = lambda **kwargs: obj.add(**kwargs)
