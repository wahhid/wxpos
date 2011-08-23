import pos.db
db = pos.db.db

import pos.modules.base.objects.common as common

class Customergroup(common.Item):
    data_keys = ('name', 'comment')
    
    def __init__(self, _id):
        common.Item.__init__(self, _id)
        self.obj = obj
    
    def getData(self):
        self.data['name'], self.data['comment'] = \
            db.getCustomergroupInfo(self.id)

class CustomergroupObject(common.Object):
    item = Customergroup
    dbGetAll = lambda self: db.getAllCustomergroups()
    def dbInsert(self, **kwargs):
        ret = db.insertCustomergroup(**kwargs)
        return ret

    def dbUpdate(self, _id, **kwargs):
        ret = db.updateCustomergroup(_id, **kwargs)
        return ret
    
    def dbDelete(self, _id):
        ret = db.deleteCustomergroup(_id)
        return ret

    def getDBData(self, key, val):
        return val

obj = CustomergroupObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
getAll = lambda refresh=False: obj.getAll()
add = lambda **kwargs: obj.add(**kwargs)
