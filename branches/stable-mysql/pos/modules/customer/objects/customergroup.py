import pos

import pos.modules.base.objects.common as common

class Customergroup(common.Item):
    data_keys = ('name', 'comment')
    
    def getData(self):
        sql = "SELECT name, comment FROM customergroups WHERE id=%s AND state>0"
        params = (self.id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                self.data['name'], self.data['comment'] = results

class CustomergroupObject(common.Object):
    item = Customergroup
    def dbGetAll(self):
        sql = "SELECT id FROM customergroups WHERE state>0"
        params = None
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None
    
    def dbInsert(self, name, comment):
        sql = "INSERT INTO customergroups (name, comment) VALUES (%s, %s)"
        params = (name, comment)
        cursor, success = pos.db.query(sql, params)
        if success:
            _id = pos.db.conn.insert_id()
            return _id
        else:
            return None

    def dbUpdate(self, _id, **kwargs):
        fields = ('name', 'comment')
        update_str = ",".join([f+"=%s" for f in fields if kwargs.has_key(f)])
        update_params = [kwargs[f] for f in fields if kwargs.has_key(f)]
        
        if len(update_str) == 0: return True
        sql = "UPDATE customergroups SET "+update_str+" WHERE id=%s AND state>0"
        params = update_params+[_id]
        cursor, success = pos.db.query(sql, params)
        if success:
            return True
        else:
            return None
    
    def dbDelete(self, _id):
        sql = "UPDATE customergroups SET state=-1 WHERE id=%s"
        params = (_id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def getDBData(self, key, val):
        return key, val

obj = CustomergroupObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
add = lambda **kwargs: obj.add(**kwargs)
