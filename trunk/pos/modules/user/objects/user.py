import pos

import pos.modules.base.objects.common as common

import pos.modules.user.objects.role as role

class User(common.Item):
    data_keys = ('username', 'password', 'role')
    
    def __init__(self, _id, obj):
        common.Item.__init__(self, _id, obj)
        self.__logged_in = False
    
    def getData(self):
        sql = "SELECT username, role_id FROM users WHERE state>0 AND id=%s"
        params = (self.id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchall()
            if len(results)>0:
                self.data['username'], role_id = results[0]
                self.data['role'] = role.find(_id=role_id)

    def login(self, password):
        if self.isLoggedIn():
            return True
        sql = "SELECT COUNT(id) FROM users WHERE state>0 AND id=%s AND password=MD5(%s)"
        params = (self.id, password)
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchone()
            self.__logged_in = (results[0] == 1)
        else:
            self.__logged_in = False
        return self.__logged_in

    def isLoggedIn(self):
        return bool(self.__logged_in)

class UserObject(common.Object):
    item = User
    def dbGetAll(self):
        sql = "SELECT id FROM users WHERE state>0"
        params = None
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None
    
    def dbInsert(self, username, password, role_id):
        sql = "INSERT INTO users (username, password, role_id) VALUES (%s, MD5(%s), %s)"
        params = (username, password, role_id)
        cursor, success = pos.db.query(sql, params)
        if success:
            _id = pos.db.conn.insert_id()
            return _id
        else:
            return None
    
    def dbUpdate(self, _id, **kwargs):
        update = []
        if password is not None: update.append("password=MD5(%s)")
        if role_id is not None: update.append("role_id=%s")
        if len(update) == 0: return True
        update_str = ",".join(update)
        
        sql = "UPDATE users SET "+update_str+" WHERE id=%s AND state>0"
        params = [par for par in (password, role_id) if par is not None]
        params.append(user_id)
        cursor, success = pos.db.query(sql, params)
        if success:
            return True
        else:
            return None
    
    def dbDelete(self, _id):
        sql = "UPDATE users SET state=-1 WHERE id=%s"
        params = (_id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def getDBData(self, key, val):
        if key == 'role':
            return 'role_id', val.id
        else:
            return key, val

obj = UserObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
add = lambda **kwargs: obj.add(**kwargs)

current = None
