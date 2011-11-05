import traceback

db_used = 'mysql' #'sqlite'

if db_used == 'mysql':
    from .mysql import MysqlDB
    import ConfigParser
    
    class DB(MysqlDB):
        def __init__(self):
            MysqlDB.__init__(self)
            default_config = {'hostname': '', 'port': '',
                      'username': '', 'password': '',
                      'db_name': ''}

            config = ConfigParser.SafeConfigParser(default_config)
            config.read('wxpos.cfg')

            if not config.has_section('MySQL'):
                config.add_section('MySQL')
        
            self.host = config.get('MySQL', 'hostname')
            self.port = config.get('MySQL', 'port')
            self.username = config.get('MySQL', 'username')
            self.password = config.get('MySQL', 'password')
            self.db_name = config.get('MySQL', 'db_name')
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
