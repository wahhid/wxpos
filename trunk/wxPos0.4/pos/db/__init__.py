from .mysql import MysqlDB

class DB(MysqlDB):
    def __init__(self):
        MysqlDB.__init__(self)
        self.host = "localhost"
        self.username, self.password = "root", "pass"
        self.db_name = "test_pyPOS"
        self.connect()

    def error(self, error, context=None, params=None, **info):
        print '----------'
        print 'In', context, params
        if info.has_key('query'):
            print 'Query:', info['query']
        print 'Error:', error.__class__.__name__, error
        print '----------'
        raise
