import pos

import pos.modules.base.objects.common as common

import pos.modules.sales.objects.ticket as ticket

import pos.modules.stock.objects.product as product

class Ticketline(common.Item):
    data_keys = ('description', 'sell_price', 'amount',
                 'ticket', 'product', 'is_edited')
    
    def getData(self):
        sql = "SELECT description, sell_price, amount,"+\
                        " ticket_id, product_id, is_edited"+\
                " FROM ticketlines WHERE id=%s"
        params = (self.id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                self.data['description'], self.data['sell_price'], \
                    self.data['amount'], ticket_id, product_id, \
                    self.data['is_edited'] = results
        self.data['ticket'] = ticket.find(_id=ticket_id)
        if product_id is not None:
            self.data['product'] = product.find(_id=product_id)
        else:
            self.data['product'] = None

class TicketlineObject(common.Object):
    item = Ticketline
    def dbGetAll(self):
        sql = "SELECT id FROM ticketlines"
        params = None
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None
    
    def dbInsert(self, description, sell_price, amount, ticket_id, product_id, is_edited):
        sql = "INSERT INTO ticketlines"+\
            " (description, sell_price, amount, ticket_id, product_id, is_edited)"+\
            " VALUES (%s, %s, %s, %s, %s, %s)"

        params = (description, sell_price, amount, ticket_id, product_id, is_edited)
        cursor, success = pos.db.query(sql, params)
        if success:
            _id = pos.db.conn.insert_id()
            return _id
        else:
            return None
    
    def dbUpdate(self, _id, **kwargs):
        fields = ('description', 'sell_price', 'amount', 'is_edited')
        update_str = ",".join([f+"=%s" for f in fields if kwargs.has_key(f)])
        update_params = [kwargs[f] for f in fields if kwargs.has_key(f)]
        
        if len(update_str) == 0: return True
        sql = "UPDATE ticketlines SET "+update_str+" WHERE id=%s"
        params = update_params+[_id]
        cursor, success = pos.db.query(sql, params)
        if success:
            return True
        else:
            return None
    
    def dbDelete(self, _id):
        sql = "DELETE FROM ticketlines WHERE id=%s"
        params = (_id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def getDBData(self, key, val):
        if key == 'product':
            if val is None:
                return 'product_id', None
            else:
                return 'product_id', val.id
        elif key == 'ticket':
            return 'ticket_id', val.id
        else:
            return key, val

obj = TicketlineObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
add = lambda **kwargs: obj.add(**kwargs)
