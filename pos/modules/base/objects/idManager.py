from wx import NewId

class IdManager(dict):

    def __missing__(self, key):
        id = NewId()
        dict.__setitem__(self, key, id)
        return id

def init():
    global ids
    ids = IdManager()
