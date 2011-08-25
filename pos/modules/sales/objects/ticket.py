import pos.db
db = pos.db.db

import pos.modules.base.objects.common as common

import pos.modules.user.objects.user as user

import pos.modules.customer.objects.customer as customer

class Ticket(common.Item):
    data_keys = ('user', 'closed', 'customer')
    
    def __init__(self, _id):
        common.Item.__init__(self, _id)
        self.obj = obj
    
    def getData(self):
        user_id = db.getTicketUser(self.id)
        self.data['user'] = user.find(_id=user_id)

        self.data['closed'] = db.ticketIsClosed(self.id)

        customer_id = db.getTicketCustomer(self.id)
        if customer_id is None:
            self.data['customer'] = None
        else:
            self.data['customer'] = customer.find(_id=customer_id)

    def close(self):
        success = db.closeTicket(self.id)
        getAll(refresh=True)
        return bool(success)

    def setCustomer(self, c):
        success = db.setTicketCustomer(self.id, c.id)
        getAll(refresh=True)
        return bool(success)

class TicketObject(common.Object):
    item = Ticket
    dbGetAll = lambda self: db.getAllTickets()
    def dbInsert(self, **kwargs):
        ret = db.insertTicket(user_id=kwargs['user'])
        return ret
    
    def dbUpdate(self, _id, **kwargs):
        return None
    
    def dbDelete(self, _id):
        ret = db.deleteTicket(_id)
        return ret

    def getDBData(self, key, val):
        if key == 'user':
            return val.id
        else:
            return val

obj = TicketObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
getAll = lambda refresh=False: obj.getAll()
add = lambda **kwargs: obj.add(**kwargs)
