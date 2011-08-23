import pos.db
db = pos.db.db

import pos.modules.base.objects.common as common

import pos.modules.customer.objects.customergroup as customergroup

class Customer(common.Item):
    data_keys = ('name', 'code', 'first_name', 'last_name',
                 'max_debt', 'comment', 'groups')
    
    def __init__(self, _id):
        common.Item.__init__(self, _id)
        self.obj = obj
    
    def getData(self):
        self.data['name'], self.data['code'], \
            self.data['first_name'], self.data['last_name'], \
            self.data['max_debt'], self.data['comment'] = \
            db.getCustomerInfo(self.id)

        group_ids = db.getCustomerGroups(self.id)
        self.data['groups'] = map(lambda _id: customergroup.find(_id=_id), group_ids)

class CustomerObject(common.Object):
    item = Customer
    dbGetAll = lambda self: db.getAllCustomers()
    def dbInsert(self, **kwargs):
        kw = kwargs.copy()
        if kw.has_key('groups'):
            kw['group_ids'] = kwargs['groups']
            del kw['groups']
        ret = db.insertCustomer(**kw)
        return ret

    def dbUpdate(self, _id, **kwargs):
        kw = kwargs.copy()
        if kw.has_key('groups'):
            kw['group_ids'] = kwargs['groups']
            del kw['groups']
        ret = db.updateCustomer(_id, **kw)
        return ret
    
    def dbDelete(self, _id):
        ret = db.deleteCustomer(_id)
        return ret

    def getDBData(self, key, val):
        if key == 'groups':
            return map(lambda cg: cg.id, val)
        else:
            return val

obj = CustomerObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
getAll = lambda refresh=False: obj.getAll()
add = lambda **kwargs: obj.add(**kwargs)
