import pos.db
db = pos.db.db

import pos.modules.base.objects.common as common

import pos.modules.sales.objects.ticket as ticket

import pos.modules.stock.objects.product as product

class Ticketline(common.Item):
    data_keys = ('description', 'sell_price', 'amount',
                 'ticket', 'product', 'is_edited')
    
    def __init__(self, _id):
        common.Item.__init__(self, _id)
        self.obj = obj
    
    def getData(self):
        self.data['description'], self.data['sell_price'], \
            self.data['amount'], ticket_id, product_id, \
            self.data['is_edited'] = db.getTicketlineInfo(self.id)
        self.data['ticket'] = ticket.find(_id=ticket_id)
        if product_id is not None:
            self.data['product'] = product.find(_id=product_id)
        else:
            self.data['product'] = None

class TicketlineObject(common.Object):
    item = Ticketline
    dbGetAll = lambda self: db.getAllTicketlines()
    def dbInsert(self, **kwargs):
        ret = db.insertTicketline(description=kwargs['description'],
                                  sell_price=kwargs['sell_price'],
                                  amount=kwargs['amount'],
                                  ticket_id=kwargs['ticket'],
                                  product_id=kwargs['product'],
                                  is_edited=kwargs['is_edited'])
        return ret
    
    def dbUpdate(self, _id, **kwargs):
        allowed = ('description', 'sell_price', 'amount', 'is_edited')
        kw = {}
        for key in allowed:
            if kwargs.has_key(key):
                kw[key] = kwargs[key]
        ret = db.updateTicketline(_id, **kw)
        return ret
    
    def dbDelete(self, _id):
        ret = db.deleteTicketline(_id)
        return ret

    def getDBData(self, key, val):
        if key == 'product':
            if val is None:
                return None
            else:
                return val.id
        elif key == 'ticket':
            return val.id
        else:
            return val

obj = TicketlineObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
getAll = lambda refresh=False: obj.getAll()
add = lambda **kwargs: obj.add(**kwargs)
