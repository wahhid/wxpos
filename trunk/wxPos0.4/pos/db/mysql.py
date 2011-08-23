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
        self.query("clearDB", "DROP DATABASE IF EXISTS %s" % (self.db_name,))
        self.query("recreateDB", "CREATE DATABASE %s" % (self.db_name,))
        self.conn.select_db(self.db_name)

    def createTable(self, name, query):
        #self.query("createTable", "DROP TABLE IF EXISTS %s" % (name,))
        self.query("createTable", "CREATE TABLE %s (%s)" % (name, query))
    
    def query(self, func_name, sql, params=None, many=False):
        """ Creates a cursor and executes one or many queries.
            Returns (cursor, success). Success is False if an error occured.
        """
        if params is None:
            params = tuple()
        if not self.isConnected():
            self.error(None, func_name, params, query=sql)
            return None
        cursor = self.conn.cursor()
        try:
            if many:
                cursor.executemany(sql, params)
            else:
                cursor.execute(sql, params)
        except MySQLdb.Error, err:
            self.error(err, func_name, params, query=sql)
            return cursor, False
        except Exception, err:
            self.error(err, func_name, params, query=sql)
            return cursor, False
        else:
            return cursor, True
