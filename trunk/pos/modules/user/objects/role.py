import pos.db
db = pos.db.db

import pos.modules.base.objects.common as common

import pos.modules.user.objects.permission as permission

class Role(common.Item):
    data_keys = ('name', 'permissions')
    
    def __init__(self, _id):
        common.Item.__init__(self, _id)
        self.obj = obj
    
    def getData(self):
        self.data['name'] = db.getRoleName(self.id)

        permission_ids = db.getRolePermissions(self.id)
        self.data['permissions'] = map(lambda _id: permission.find(_id=_id), permission_ids)

    def isPermitted(self, permission):
        return (permission is None) or (permission in self.data['permissions'])

class RoleObject(common.Object):
    item = Role
    dbGetAll = lambda self: db.getAllRoles()
    def dbInsert(self, **kwargs):
        ret = db.insertRole(name=kwargs['name'],
                            permission_ids=kwargs['permissions'])
        return ret
    
    def dbUpdate(self, _id, **kwargs):
        ret = db.updateRole(_id, permission_ids=kwargs['permissions'])
        return ret
    
    def dbDelete(self, _id):
        ret = db.deleteRole(_id)
        return ret

    def getDBData(self, key, val):
        if key == 'permissions':
            return map(lambda p: p.id, val)
        else:
            return val

obj = RoleObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
getAll = lambda refresh=False: obj.getAll()
add = lambda **kwargs: obj.add(**kwargs)
