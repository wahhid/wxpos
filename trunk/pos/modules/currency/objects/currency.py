import pos.db
db = pos.db.db

import pos.modules.base.objects.common as common

class Currency(common.Item):
    data_keys = ('name', 'symbol', 'value')
    
    def __init__(self, _id):
        common.Item.__init__(self, _id)
        self.obj = obj
    
    def getData(self):
        self.data['name'], self.data['symbol'], self.data['value'] = \
                           db.getCurrencyInfo(self.id)

class CurrencyObject(common.Object):
    item = Currency
    dbGetAll = lambda self: db.getAllCurrencies()
    def dbInsert(self, **kwargs):
        ret = db.insertCurrency(name=kwargs['name'],
                                symbol=kwargs['symbol'],
                                value=kwargs['value'])
        return ret
    
    def dbUpdate(self, _id, **kwargs):
        ret = db.updateCurrency(_id, name=kwargs['name'],
                                symbol=kwargs['symbol'],
                                value=kwargs['value'])
        return ret
    
    def dbDelete(self, _id):
        ret = db.deleteCurrency(_id)
        return ret

    def getDBData(self, key, val):
        if key == 'value':
            return float(val)
        else:
            return val

obj = CurrencyObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
getAll = lambda refresh=False: obj.getAll()
add = lambda **kwargs: obj.add(**kwargs)

default = find(_id=1)

def convert(price, src_currency, dest_currency):
    s_val = float(src_currency.data['value'])
    d_val = float(dest_currency.data['value'])
    #ps*vs = pd*vd

    return float(price)*s_val/d_val
