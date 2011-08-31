class BaseDB:

    def __init__(self):
        self.conn = None
        self.__closed = False
        self.__sub = {}
    
    def connect(self):
        self.__closed = False
    def isConnected(self):
        return self.conn is not None
    
    def close(self):
        self.__closed = True
    def isClosed(self):
        return bool(self.__closed)

    def clear(self):
        pass
    def query(self, query, params=None, many=False):
        """ Creates a cursor and executes one or many queries.
            Returns (cursor, success). Success is False if an error occured.
        """
        if params is None:
            params = tuple()
        if not self.isConnected():
            return None

        try:
            cursor = self.executeQuery(query, params, many)
        except:
            self.error(query, params, many)
            return cursor, False
        else:
            return cursor, True
    
    def extend(self, sub_dbs):
        self.__sub.update(sub_dbs)
    
    def __del__(self):
        self.close()

    def __getattr__(self, name):
        try:
            attr = object.__getattr__(self, name)
        except AttributeError:
            if self.__sub.has_key(name):
                return self.__sub[name]
            else:
                raise
        else:
            return attr
    
    def error(self, query=None, params=None, many=None):
        raise
