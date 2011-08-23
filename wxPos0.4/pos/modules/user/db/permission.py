class PermissionDB:
    def insertPermission(self, name, description):
        sql = "INSERT INTO permissions (name, description) VALUES (%s, %s)"
        params = (name, description)
        cursor, success = self.db.query('insertPermission', sql, params)
        if success:
            permission_id = self.conn.insert_id()
            return permission_id
        else:
            return None

    def updatePermission(self, permission_id, description):
        sql = "UPDATE permissions SET description=%s WHERE id=%s"
        params = (description, permission_id)
        cursor, success = self.db.query('updatePermission', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def deletePermission(self, permission_id):
        sql = "DELETE FROM permissions WHERE id=%s"
        params = (permission_id,)
        cursor, success = self.db.query('deletePermission', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def getAllPermissions(self):
        sql = "SELECT id FROM permissions"
        params = None
        cursor, success = self.db.query('getAllPermissions', sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None
    
    def getPermissionInfo(self, permission_id):
        sql = "SELECT name, description FROM permissions WHERE id=%s"
        params = (permission_id,)
        cursor, success = self.db.query('getPermissionInfo', sql, params)
        if success:
            results = cursor.fetchall()
            if len(results)>0:
                return results[0]
            else:
                return None
        else:
            return None
