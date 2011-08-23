class CustomerDB:
    def getAllCustomers(self):
        sql = "SELECT id FROM customers WHERE state>0"
        params = None
        cursor, success = self.db.query('getAllCustomers', sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None

    def insertCustomer(self, name, code, first_name, last_name,
                           max_debt, comment, group_ids):
        sql = """INSERT INTO customers
            (name, code, first_name, last_name, max_debt, comment)
        VALUES (%s, %s, %s, %s, %s, %s)
"""
        params = (name, code, first_name, last_name, max_debt, comment)
        cursor, success = self.db.query('insertCustomer', sql, params)
        if success:
            customer_id = self.conn.insert_id()
        else:
            return None

        if len(group_ids)>0:
            sql2 = "INSERT INTO customer_group (customer_id, group_id) VALUES (%s, %s)"
            params2 = [(customer_id, cg_id) for cg_id in group_ids]
            cursor2, success2 = self.db.query('insertCustomer', sql2, params2, many=True)
            if success2 and cursor2.rowcount > 0:
                return customer_id
            else:
                return None

    def updateCustomer(self, customer_id, name=None, code=None,
                      first_name=None, last_name=None, max_debt=None,
                      comment=None, group_ids=None):
        fields = ('name', 'code', 'first_name', 'last_name', 'max_debt', 'comment')
        update_str = [f+"=%s" for f in fields if locals()[f] is not None]
        if len(update_str) > 0:
            sql = "UPDATE customers SET "+",".join(update_str)+" WHERE id=%s AND state>0"
            params = [locals()[f] for f in fields if locals()[f] is not None]
            params.append(customer_id)
            cursor, success = self.db.query('updateCustomer', sql, params)

            if not success or cursor.rowcount != 1:
                return None

        if group_ids is not None:
            return self.__updateCustomerGroups(customer_id, group_ids)
        else:
            return True

    def __updateCustomerGroups(self, customer_id, group_ids):
        sql = "DELETE FROM customer_group WHERE customer_id=%s"
        params = (customer_id,)
        cursor, success = self.db.query('updateCustomer', sql, params)
        if not success:
            return None
        
        if len(group_ids)>0:
            sql2 = "INSERT INTO customer_group (customer_id, group_id) VALUES (%s, %s)"
            params2 = [(customer_id, cg_id) for cg_id in group_ids]
            cursor2, success2 = self.db.query('updateCustomer', sql2, params2, many=True)
            if success2:
                return cursor2.rowcount > 0
            else:
                return None

    def deleteCustomer(self, customer_id):
        sql = "UPDATE customers SET state=-1 WHERE id=%s"
        params = (customer_id,)
        cursor, success = self.db.query('deleteCustomer', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None
    
    def getCustomerInfo(self, customer_id):
        sql = """SELECT name, code, first_name, last_name, max_debt, comment
                FROM customers WHERE id=%s AND state>0
"""
        params = (customer_id,)
        cursor, success = self.db.query('getCustomerInfo', sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                return results
            else:
                return None
        else:
            return None

    def getCustomerGroups(self, customer_id):
        sql = "SELECT group_id FROM customer_group WHERE customer_id=%s"
        params = (customer_id,)
        cursor, success = self.db.query('getCustomerGroups', sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None
