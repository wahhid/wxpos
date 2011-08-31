import pos

import pos.modules.base.objects.common as common

import pos.modules.customer.objects.customergroup as customergroup

class Customer(common.Item):
    data_keys = ('name', 'code', 'first_name', 'last_name',
                 'max_debt', 'comment', 'groups')
    
    def getData(self):
        sql = "SELECT name, code, first_name, last_name, max_debt, comment"+\
                " FROM customers WHERE id=%s AND state>0"
        params = (self.id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                self.data['name'], self.data['code'], \
                    self.data['first_name'], self.data['last_name'], \
                    self.data['max_debt'], self.data['comment'] = results

        sql = "SELECT group_id FROM customer_group WHERE customer_id=%s"
        params = (self.id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchall()
            group_ids = map(lambda r: r[0], results)

        self.data['groups'] = map(lambda _id: customergroup.find(_id=_id), group_ids)

class CustomerObject(common.Object):
    item = Customer
    def dbGetAll(self):
        sql = "SELECT id FROM customers WHERE state>0"
        params = None
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None
    
    def dbInsert(self, name, code, first_name, last_name,
                            max_debt, comment, group_ids):
        sql = """INSERT INTO customers
            (name, code, first_name, last_name, max_debt, comment)
        VALUES (%s, %s, %s, %s, %s, %s)
"""
        params = (name, code, first_name, last_name, max_debt, comment)
        cursor, success = pos.db.query(sql, params)
        if success:
            _id = pos.db.conn.insert_id()
        else:
            return None

        if len(group_ids)>0:
            sql2 = "INSERT INTO customer_group (customer_id, group_id) VALUES (%s, %s)"
            params2 = [(_id, cg_id) for cg_id in group_ids]
            cursor2, success2 = pos.db.query(sql2, params2, many=True)
            if success2 and cursor2.rowcount > 0:
                return _id
            else:
                return None

    def dbUpdate(self, _id, **kwargs):
        fields = ('name', 'code', 'first_name', 'last_name', 'max_debt', 'comment')
        update_str = ",".join([f+"=%s" for f in fields if kwargs.has_key(f)])
        update_params = [kwargs[f] for f in fields if kwargs.has_key(f)]
        if len(update_str) > 0:
            sql = "UPDATE customers SET "+update_str+" WHERE id=%s AND state>0"
            params = update_params+[_id]
            cursor, success = pos.db.query(sql, params)

            if not success:
                return None

        if kwargs.has_key('group_ids'):
            sql = "DELETE FROM customer_group WHERE customer_id=%s"
            params = (_id,)
            cursor, success = pos.db.query(sql, params)
            if not success:
                return None
            
            if len(kwargs['group_ids'])>0:
                sql2 = "INSERT INTO customer_group (customer_id, group_id) VALUES (%s, %s)"
                params2 = [(_id, cg_id) for cg_id in kwargs['group_ids']]
                cursor2, success2 = pos.db.query(sql2, params2, many=True)
                if success2:
                    return cursor2.rowcount > 0
                else:
                    return None
        else:
            return True
    
    def dbDelete(self, _id):
        sql = "UPDATE customers SET state=-1 WHERE id=%s"
        params = (_id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def getDBData(self, key, val):
        if key == 'groups':
            return 'group_ids', map(lambda cg: cg.id, val)
        else:
            return key, val

obj = CustomerObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
add = lambda **kwargs: obj.add(**kwargs)
