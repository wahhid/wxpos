import pos

import pos.modules.base.objects.common as common

class Permission(common.Item):
    data_keys = ('name', 'description')
    
    def getData(self):
        sql = "SELECT name, description FROM permissions WHERE id=%s"
        params = (self.id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                self.data['name'], self.data['description'] = results

class PermissionObject(common.Object):
    item = Permission
    def dbGetAll(self):
        sql = "SELECT id FROM permissions"
        params = None
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None

    def dbInsert(self, **kwargs):
        sql = "INSERT INTO permissions (name, description) VALUES (%s, %s)"
        params = (name, description)
        cursor, success = pos.db.query(sql, params)
        if success:
            _id = pos.db.conn.insert_id()
            return _id
        else:
            return None
    
    def dbUpdate(self, _id, **kwargs):
        fields = ('description',)
        update_str = ",".join([f+"=%s" for f in fields if kwargs.has_key(f)])
        update_params = [kwargs[f] for f in fields if kwargs.has_key(f)]
        
        if len(update_str) == 0: return True
        sql = "UPDATE permissions SET "+update_str+" WHERE id=%s"
        params = update_params+[_id]
        cursor, success = self.db.query(sql, params)
        if success:
            return True
        else:
            return None
    
    def dbDelete(self, _id):
        sql = "DELETE FROM permissions WHERE id=%s"
        params = (_id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def getDBData(self, key, val):
        return key, val

obj = PermissionObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
add = lambda **kwargs: obj.add(**kwargs)
