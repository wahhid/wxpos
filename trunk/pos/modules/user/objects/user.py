import pos.db
db = pos.db.db

import pos.modules.base.objects.common as common

import pos.modules.user.objects.role as role

class User(common.Item):
    data_keys = ('username', 'password', 'role')
    
    def __init__(self, _id):
        common.Item.__init__(self, _id)
        self.obj = obj
        self.__logged_in = False
    
    def getData(self):
        self.data['username'] = db.getUsername(self.id)
        
        role_id = db.getUserRole(self.id)
        if role_id is None:
            self.data['role'] = None
        else:
            self.data['role'] = role.find(_id=role_id)

    def login(self, password):
        if self.isLoggedIn():
            return True
        self.__logged_in = db.loginUser(self.id, password)
        return self.__logged_in

    def isLoggedIn(self):
        return self.__logged_in

class UserObject(common.Object):
    item = User
    dbGetAll = lambda self: db.getAllUsers()
    def dbInsert(self, **kwargs):
        ret = db.insertUser(username=kwargs['username'],
                            password=kwargs['password'],
                            role_id=kwargs['role'])
        return ret
    
    def dbUpdate(self, _id, **kwargs):
        kw = {}
        if kwargs.has_key('password'):
            kw['password'] = kwargs['password']
        if kwargs.has_key('role'):
            kw['role_id'] = kwargs['role']
        ret = db.updateUser(_id, **kw)
        return ret
    
    def dbDelete(self, _id):
        ret = db.deleteUser(_id)
        return ret

    def getDBData(self, key, val):
        if key == 'role':
            if val is None:
                return None
            else:
                return val.id
        else:
            return val

obj = UserObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
getAll = lambda refresh=False: obj.getAll()
add = lambda **kwargs: obj.add(**kwargs)

current = None
