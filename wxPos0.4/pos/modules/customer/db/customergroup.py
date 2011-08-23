class CustomergroupDB:
    def getAllCustomergroups(self):
        sql = "SELECT id FROM customergroups WHERE state>0"
        params = None
        cursor, success = self.db.query('getAllCustomergroups', sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None

    def insertCustomergroup(self, name, comment):
        sql = "INSERT INTO customergroups (name, comment) VALUES (%s, %s)"
        params = (name, comment)
        cursor, success = self.db.query('insertCustomergroup', sql, params)
        if success:
            customergroup_id = self.conn.insert_id()
            return customergroup_id
        else:
            return None

    def updateCustomergroup(self, customergroup_id, name=None, comment=None):
        fields = ('name', 'comment')
        update_str = [f+"=%s" for f in fields if locals()[f] is not None]
        if len(update_str) == 0: return None
        
        sql = "UPDATE customergroups SET "+",".join(update_str)+" WHERE id=%s AND state>0"
        params = [locals()[f] for f in fields if locals()[f] is not None]
        params.append(customergroup_id)
        cursor, success = self.db.query('updateCustomergroup', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def deleteCustomergroup(self, customergroup_id):
        sql = "UPDATE customergroups SET state=-1 WHERE id=%s"
        params = (customergroup_id,)
        cursor, success = self.db.query('deleteCustomergroup', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None
    
    def getCustomergroupInfo(self, customergroup_id):
        sql = "SELECT name, comment FROM customergroups WHERE id=%s AND state>0"
        params = (customergroup_id,)
        cursor, success = self.db.query('getCustomergroupInfo', sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                return results
            else:
                return None
        else:
            return None
