from .base import BaseDB
import sqlite3

class SqliteDB(BaseDB):
    def __init__(self):
        BaseDB.__init__(self)
        self.db_name = None
    
    def connect(self):
        if not self.isConnected():
            try:
                self.conn = sqlite3.connect(self.db_name)
            except sqlite3.Error, err:
                self.error(err, 'connect', (self.db_name))
                return False
            else:
                BaseDB.connect(self)
                return True
        else:
            return True
    
    def close(self):
        if not self.isClosed():
            self.conn.close()
            BaseDB.close(self)

    def clear(self):
        pass
    
    def executeQuery(self, query, params, many):
        cursor = self.conn.cursor()
        if many:
            cursor.executemany(query, params)
        else:
            cursor.execute(query, params)
        self.conn.commit()
        return cursor
