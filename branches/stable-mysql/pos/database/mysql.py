from .base import BaseDB
import MySQLdb

class MysqlDB(BaseDB):
    def __init__(self):
        BaseDB.__init__(self)
        self.host = None
        self.username, self.password = None, None
        self.db_name = None
    
    def connect(self):
        if not self.isConnected():
            try:
                self.conn = MySQLdb.connect(self.host, self.username, self.password, self.db_name)
            except MySQLdb.Error, err:
                self.error(err, 'connect', (self.host, self.username, self.password, self.db_name))
                return False
            else:
                self.conn.autocommit(True)
                BaseDB.connect(self)
                return True
        else:
            return True
    
    def close(self):
        if not self.isClosed():
            self.conn.close()
            BaseDB.close(self)

    def clear(self):
        self.query("DROP DATABASE IF EXISTS %s" % (self.db_name,))
        self.query("CREATE DATABASE %s" % (self.db_name,))
        self.conn.select_db(self.db_name)
    
    def executeQuery(self, query, params, many):
        cursor = self.conn.cursor()
        if many:
            cursor.executemany(query, params)
        else:
            cursor.execute(query, params)
        return cursor
