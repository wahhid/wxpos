from .mysql import MysqlDB

import traceback

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
