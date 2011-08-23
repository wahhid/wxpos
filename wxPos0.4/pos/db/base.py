class BaseDB:

    def __init__(self):
        self.conn = None
        self.__closed = False
        self.__sub = []
    
    def connect(self):
        self.__closed = False
    def isConnected(self):
        return self.conn is not None
    
    def close(self):
        self.__closed = True
    def isClosed(self):
        return bool(self.__closed)

    def extend(self, sub_db):
        self.__sub.append(sub_db(self))
    
    def __del__(self):
        self.close()

    def __getattr__(self, name):
        try:
            attr = object.__getattr__(self, name)
        except AttributeError:
            for sub in self.__sub:
                try:
                    attr = getattr(sub, name)
                except AttributeError:
                    pass
                else:
                    break
            else:
                raise AttributeError, name
            return attr
        else:
            return attr
    
    def error(self, error, context=None, params=None, **info):
        raise
