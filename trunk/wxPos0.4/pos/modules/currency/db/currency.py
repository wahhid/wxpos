class CurrencyDB:
    def getAllCurrencies(self):
        sql = "SELECT id FROM currencies"
        params = None
        cursor, success = self.db.query('getAllCurrencies', sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None

    def insertCurrency(self, name, symbol, value):
        sql = "INSERT INTO currencies (name, symbol, value) VALUES (%s, %s, %s)"
        params = (name, symbol, value)
        cursor, success = self.db.query('insertCurrency', sql, params)
        if success:
            category_id = self.conn.insert_id()
            return category_id
        else:
            return None

    def updateCurrency(self, currency_id, name=None, symbol=None, value=None):
        update_str = []
        if name is not None: update_str.append("name=%s")
        if symbol is not None: update_str.append("symbol=%s")
        if value is not None: update_str.append("value=%s")
        if len(update_str) == 0: return None
        
        sql = "UPDATE currencies SET "+",".join(update_str)+" WHERE id=%s"
        params = [par for par in (name, symbol, value) if par is not None]
        params.append(currency_id)
        cursor, success = self.db.query('updateCurrency', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def deleteCurrency(self, currency_id):
        sql = "DELETE FROM currencies WHERE id=%s"
        params = (currency_id,)
        cursor, success = self.db.query('deleteCurrency', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None
    
    def getCurrencyInfo(self, currency_id):
        sql = "SELECT name, symbol, value FROM currencies WHERE id=%s"
        params = (currency_id,)
        cursor, success = self.db.query('getCurrencyInfo', sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                return results
            else:
                return None
        else:
            return None
