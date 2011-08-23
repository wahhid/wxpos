import pos.db
db = pos.db.db

import pos.modules.base.objects.common as common

class Permission(common.Item):
    data_keys = ('name', 'description')
    
    def __init__(self, _id):
        common.Item.__init__(self, _id)
        self.obj = obj
    
    def getData(self):
        self.data['name'], self.data['description'] = \
                           db.getPermissionInfo(self.id)

class PermissionObject(common.Object):
    item = Permission
    dbGetAll = lambda self: db.getAllPermissions()
    def dbInsert(self, **kwargs):
        ret = db.insertPermission(name=kwargs['name'],
                                  description=kwargs['description'])
        return ret
    
    def dbUpdate(self, _id, **kwargs):
        ret = db.updatePermission(_id, description=kwargs['description'])
        print _id, kwargs, ret
        return ret
    
    def dbDelete(self, _id):
        ret = db.deletePermission(_id)
        return ret

    def getDBData(self, key, val):
        return val

obj = PermissionObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
getAll = lambda refresh=False: obj.getAll()
add = lambda **kwargs: obj.add(**kwargs)
