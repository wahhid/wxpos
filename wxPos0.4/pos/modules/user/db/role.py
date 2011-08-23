class RoleDB:
    def getAllRoles(self):
        sql = "SELECT id FROM roles"
        params = None
        cursor, success = self.db.query('getAllRoles', sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None

    def insertRole(self, name, permission_ids):
        sql = "INSERT INTO roles (name) VALUES (%s)"
        params = (name,)
        cursor, success = self.db.query('insertRole', sql, params)
        if success:
            role_id = self.conn.insert_id()
        else:
            return None
        
        if len(permission_ids)>0:
            sql2 = "INSERT INTO role_permission (role_id, permission_id) VALUES (%s, %s)"
            params2 = [(role_id, p_id) for p_id in permission_ids]
            cursor2, success2 = self.db.query('insertRole', sql2, params2, many=True)
            if success2 and cursor2.rowcount > 0:
                return role_id
            else:
                return None

    def updateRole(self, role_id, permission_ids):
        sql = "DELETE FROM role_permission WHERE role_id=%s"
        params = (role_id,)
        cursor, success = self.db.query('updateRole', sql, params)
        if not success:
            return None
        
        if len(permission_ids)>0:
            sql2 = "INSERT INTO role_permission (role_id, permission_id) VALUES (%s, %s)"
            params2 = [(role_id, p_id) for p_id in permission_ids]
            cursor2, success2 = self.db.query('updateRole', sql2, params2, many=True)
            if success2:
                return cursor2.rowcount > 0
            else:
                return None

    def deleteRole(self, role_id):
        self.updateRole(role_id, [])
        
        sql = "DELETE FROM roles WHERE id=%s"
        params = (role_id,)
        cursor, success = self.db.query('deleteRole', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None
    
    def getRoleName(self, role_id):
        sql = "SELECT name FROM roles WHERE id=%s"
        params = (role_id,)
        cursor, success = self.db.query('getRoleName', sql, params)
        if success:
            results = cursor.fetchall()
            if len(results)>0:
                return results[0][0]
            else:
                return None
        else:
            return None

    def getRolePermissions(self, role_id):
        sql = "SELECT permission_id FROM role_permission WHERE role_id=%s"
        params = (role_id,)
        cursor, success = self.db.query('getRolePermissions', sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None
