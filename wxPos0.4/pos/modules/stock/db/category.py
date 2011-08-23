class CategoryDB:
    def getAllCategories(self):
        sql = "SELECT id FROM categories WHERE state>0"
        params = None
        cursor, success = self.db.query('getAllCategories', sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None

    def insertCategory(self, name, parent_id):
        sql = "INSERT INTO categories (name, parent_id) VALUES (%s, %s)"
        params = (name, parent_id)
        cursor, success = self.db.query('insertCategory', sql, params)
        if success:
            category_id = self.conn.insert_id()
            return category_id
        else:
            return None

    def updateCategory(self, category_id, name=None, parent_id=None):
        update_str = []
        if name is not None: update_str.append("name=%s")
        if parent_id is not None: update_str.append("parent_id=%s")
        if len(update_str) == 0: return None
        
        sql = "UPDATE categories SET "+",".join(update_str)+" WHERE id=%s AND state>0"
        params = [par for par in (name, parent_id) if par is not None]
        params.append(category_id)
        cursor, success = self.db.query('updateCategory', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def deleteCategory(self, category_id):
        sql = "UPDATE categories SET state=-1 WHERE id=%s"
        params = (category_id,)
        cursor, success = self.db.query('deleteCategory', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None
    
    def getCategoryName(self, category_id):
        sql = "SELECT name FROM categories WHERE id=%s"
        params = (category_id,)
        cursor, success = self.db.query('getCategoryName', sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                return results[0]
            else:
                return None
        else:
            return None

    def getCategoryParent(self, category_id):
        sql = "SELECT parent_id FROM categories WHERE id=%s"
        params = (category_id,)
        cursor, success = self.db.query('getCategoryParent', sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                return results[0]
            else:
                return None
        else:
            return None
