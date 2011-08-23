import pos.db
db = pos.db.db

import pos.modules.base.objects.common as common

class Category(common.Item):
    data_keys = ('name', 'parent_category')
    
    def __init__(self, _id):
        common.Item.__init__(self, _id)
        self.obj = obj
    
    def getData(self):
        self.data['name'] = db.getCategoryName(self.id)
        
        parent_id = db.getCategoryParent(self.id)
        if parent_id is None:
            self.data['parent_category'] = None
        else:
            self.data['parent_category'] = self.obj.find(_id=parent_id)

class CategoryObject(common.Object):
    item = Category
    dbGetAll = lambda self: db.getAllCategories()
    def dbInsert(self, **kwargs):
        ret = db.insertCategory(name=kwargs['name'],
                                parent_id=kwargs['parent_category'])
        return ret
    
    def dbUpdate(self, _id, **kwargs):
        ret = db.updateCategory(_id, name=kwargs['name'],
                                parent_id=kwargs['parent_category'])
        return ret
    
    def dbDelete(self, _id):
        ret = db.deleteCategory(_id)
        return ret

    def getDBData(self, key, val):
        if key == 'parent_category':
            if val is None:
                return None
            else:
                return val.id
        else:
            return val

obj = CategoryObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
getAll = lambda refresh=False: obj.getAll()
add = lambda **kwargs: obj.add(**kwargs)
