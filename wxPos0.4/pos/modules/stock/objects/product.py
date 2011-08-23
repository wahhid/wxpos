import pos.db
db = pos.db.db

import pos.modules.base.objects.common as common

import pos.modules.currency.objects.currency as currency

import pos.modules.stock.objects.category as category

class Product(common.Item):
    data_keys = ('name', 'description', 'reference', 'code',
                 'price', 'currency', 'quantity', 'category')
    
    def __init__(self, _id):
        common.Item.__init__(self, _id)
        self.obj = obj
    
    def getData(self):
        self.data['name'], self.data['description'], \
            self.data['reference'], self.data['code'], \
            self.data['price'], currency_id, \
            self.data['quantity'], category_id = \
            db.getProductInfo(self.id)
        if category_id is not None:
            self.data['category'] = category.find(_id=category_id)
        else:
            self.data['category'] = None
        self.data['currency'] = currency.find(_id=currency_id)

class ProductObject(common.Object):
    item = Product
    dbGetAll = lambda self: db.getAllProducts()
    def dbInsert(self, **kwargs):
        ret = db.insertProduct(name=kwargs['name'], description=kwargs['description'],
                               reference=kwargs['reference'], code=kwargs['code'],
                               price=kwargs['price'], currency_id=kwargs['currency'],
                               quantity=kwargs['quantity'], category_id=kwargs['category'])
        return ret

    def dbUpdate(self, _id, **kwargs):
        ret = db.updateProduct(_id, name=kwargs['name'], description=kwargs['description'],
                               reference=kwargs['reference'], code=kwargs['code'],
                               price=kwargs['price'], currency_id=kwargs['currency'],
                               quantity=kwargs['quantity'], category_id=kwargs['category'])
        return ret
    
    def dbDelete(self, _id):
        ret = db.deleteProduct(_id)
        return ret

    def getDBData(self, key, val):
        if key == 'category':
            if val is None:
                return None
            else:
                return val.id
        elif key == 'currency':
            return val.id
        else:
            return val

obj = ProductObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
getAll = lambda refresh=False: obj.getAll()
add = lambda **kwargs: obj.add(**kwargs)
