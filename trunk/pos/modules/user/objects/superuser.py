import pos

class SuperUser:
    def __init__(self):
        self.id = -1
        self.username = '_superuser_'
        self.encoded_password = ''
        self.password = ''
        self.role = SuperRole()
        
        self.display = '_superuser_'

    def login(self, password):
        # TODO the superuser password should not be hard-coded
        return (password == '_superuser_')

    def fillDict(self, D):
        for k in D.keys():
            D[k] = getattr(self, k)
    
    def update(self, **kwargs):
        return True
    
    def delete(self):
        return True

    def __repr__(self):
        return "<SuperUser %s>" % (self.username,)

class SuperRole:
    def __init__(self):
        self.id = -1
        self.name = '_superrole_'
        self.permissions = []
        
        self.display = '_superrole_'

    def isPermitted(self, permission):
        return True

    def __repr__(self):
        return "<SuperRole %s>" % (self.name,)
