class DBSubset:

    def __init__(self, db):
        self.db = db
        self.conn = self.db.conn
    
    def error(self, error, context=None, params=None, **info):
        self.db.error(error, context, params, **info)
