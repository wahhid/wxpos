import pos

import pos.modules.base.objects.common as common

import pos.modules.user.objects.permission as permission

class Role(common.Item):
    data_keys = ('name', 'permissions')

    def getData(self):
        sql = "SELECT name FROM roles WHERE id=%s"
        params = (self.id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchall()
            if len(results)>0:
                self.data['name'] = results[0][0]

        sql2 = "SELECT permission_id FROM role_permission WHERE role_id=%s"
        params2 = (self.id,)
        cursor2, success2 = pos.db.query(sql2, params2)
        if success2:
            results2 = cursor2.fetchall()
            permission_ids = map(lambda r: r[0], results2)
            self.data['permissions'] = map(lambda _id: permission.find(_id=_id), permission_ids)

    def isPermitted(self, permission):
        return (permission is None) or (permission in self.data['permissions'])

class RoleObject(common.Object):
    item = Role
    def dbGetAll(self):
        sql = "SELECT id FROM roles"
        params = None
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None
    
    def dbInsert(self, name, permission_ids):
        sql = "INSERT INTO roles (name) VALUES (%s)"
        params = (name,)
        cursor, success = pos.db.query(sql, params)
        if success:
            _id = pos.db.conn.insert_id()
        else:
            return None
        
        if len(permission_ids)>0:
            sql2 = "INSERT INTO role_permission (role_id, permission_id) VALUES (%s, %s)"
            params2 = [(role_id, p_id) for p_id in permission_ids]
            cursor2, success2 = pos.db.query(sql2, params2, many=True)
            if success2 and cursor2.rowcount > 0:
                return _id
            else:
                return None
    
    def dbUpdate(self, _id, permission_ids):
        sql = "DELETE FROM role_permission WHERE role_id=%s"
        params = (_id,)
        cursor, success = pos.db.query(sql, params)
        if not success:
            return None
        
        if len(permission_ids)>0:
            sql2 = "INSERT INTO role_permission (role_id, permission_id) VALUES (%s, %s)"
            params2 = [(role_id, p_id) for p_id in permission_ids]
            cursor2, success2 = pos.db.query(sql2, params2, many=True)
            if success2:
                return cursor2.rowcount > 0
            else:
                return None
    
    def dbDelete(self, _id):
        sql = "DELETE FROM role_permission WHERE role_id=%s"
        params = (_id,)
        cursor, success = pos.db.query(sql, params)
        if not success:
            return None
        
        sql2 = "DELETE FROM roles WHERE id=%s"
        params2 = (_id,)
        cursor2, success2 = pos.db.query(sql, params)
        if success2:
            return (cursor2.rowcount == 1)
        else:
            return None

    def getDBData(self, key, val):
        if key == 'permissions':
            return map(lambda p: p.id, val)
        else:
            return val

obj = RoleObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
add = lambda **kwargs: obj.add(**kwargs)
