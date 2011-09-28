import traceback

db_used = 'mysql' #'sqlite'

if db_used == 'mysql':
    from .mysql import MysqlDB
    
    class DB(MysqlDB):
        def __init__(self):
            MysqlDB.__init__(self)
            self.host = "localhost"
            self.username, self.password = "root", "pass"
            self.db_name = "test_pyPOS"
            self.connect()

        def error(self, query=None, params=None, many=None):
            print '----------'
            print 'Error:',
            traceback.print_exc(2)
            print 'Query:', query
            print 'Params:', params
            print 'Many:', many
            print '----------'
            print
            print
            raise
elif db_used == 'sqlite':
    from .sqlite import SqliteDB
    
    class DB(SqliteDB):
        def __init__(self):
            SqliteDB.__init__(self)
            self.db_name = "wxpos_db_test"
            self.connect()

        def error(self, query=None, params=None, many=None):
            print '----------'
            print 'Error:',
            traceback.print_exc(2)
            print 'Query:', query
            print 'Params:', params
            print 'Many:', many
            print '----------'
            print
            print
            raise
