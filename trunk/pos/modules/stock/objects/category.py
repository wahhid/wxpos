import pos

import pos.modules.base.objects.common as common

class Category(common.Item):
    data_keys = ('name', 'parent_category')

    def getData(self):
        sql = "SELECT name, parent_id FROM categories WHERE id=%s"
        params = (self.id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                self.data['name'], parent_id = results
                
                if parent_id is None:
                    self.data['parent_category'] = None
                else:
                    self.data['parent_category'] = find(_id=parent_id)

class CategoryObject(common.Object):
    item = Category
    def dbGetAll(self):
        sql = "SELECT id FROM categories WHERE state>0"
        params = None
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None
    
    def dbInsert(self, name, parent_id):
        sql = "INSERT INTO categories (name, parent_id) VALUES (%s, %s)"
        params = (name, parent_id)
        cursor, success = pos.db.query(sql, params)
        if success:
            _id = pos.db.conn.insert_id()
            return _id
        else:
            return None
    
    def dbUpdate(self, _id, **kwargs):
        fields = ('name', 'parent_id')
        update_str = ",".join([f+"=%s" for f in fields if kwargs.has_key(f)])
        update_params = [kwargs[f] for f in fields if kwargs.has_key(f)]
        
        if len(update_str) == 0: return True
        sql = "UPDATE categories SET "+update_str+" WHERE id=%s"
        params = update_params+[_id]
        cursor, success = pos.db.query(sql, params)
        if success:
            return True
        else:
            return None
    
    def dbDelete(self, _id):
        sql = "UPDATE categories SET state=-1 WHERE id=%s"
        params = (_id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def getDBData(self, key, val):
        if key == 'parent_category':
            if val is None:
                return 'parent_id', None
            else:
                return 'parent_id', val.id
        else:
            return key, val

obj = CategoryObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
add = lambda **kwargs: obj.add(**kwargs)
