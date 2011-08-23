class UserDB:
    def getAllUsers(self):
        sql = "SELECT id FROM users WHERE state>0"
        params = None
        cursor, success = self.db.query('getAllUsers', sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None

    def insertUser(self, username, password, role_id):
        sql = "INSERT INTO users  (username, password, role_id) VALUES (%s, MD5(%s), %s)"
        params = (username, password, role_id)
        cursor, success = self.db.query('insertUser', sql, params)
        if success:
            user_id = self.conn.insert_id()
            return user_id
        else:
            return None

    def updateUser(self, user_id, password=None, role_id=None):
        update_str = []
        if password is not None: update_str.append("password=MD5(%s)")
        if role_id is not None: update_str.append("role_id=%s")
        if len(update_str) == 0: return None
        
        sql = "UPDATE users SET "+",".join(update_str)+" WHERE id=%s AND state>0"
        params = [par for par in (password, role_id) if par is not None]
        params.append(user_id)
        cursor, success = self.db.query('updateUser', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def deleteUser(self, user_id):
        sql = "UPDATE users SET state=-1 WHERE id=%s"
        params = (user_id,)
        cursor, success = self.db.query('deleteUser', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None
    
    def loginUser(self, user_id, password=''):
        sql = "SELECT COUNT(id) FROM users WHERE state>0 AND id=%s AND password=MD5(%s)"
        params = (user_id, password)
        cursor, success = self.db.query('loginUser', sql, params)
        if success:
            results = cursor.fetchone()
            return results[0]
        else:
            return None

    def getUsername(self, user_id):
        sql = "SELECT username FROM users WHERE state>0 AND id=%s"
        params = (user_id,)
        cursor, success = self.db.query('getUsername', sql, params)
        if success:
            results = cursor.fetchall()
            if len(results)>0:
                return results[0][0]
            else:
                return None
        else:
            return None
    
    def getUserRole(self, user_id):
        sql = "SELECT r.id FROM users u, roles r WHERE state>0 AND u.id=%s AND r.id=u.role_id"
        params = (user_id,)
        cursor, success = self.db.query('loginUser', sql, params)
        if success:
            results = cursor.fetchall()
            if len(results)>0:
                return results[0][0]
            else:
                return None
        else:
            return None
