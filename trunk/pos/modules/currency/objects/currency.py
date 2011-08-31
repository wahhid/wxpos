import pos

import pos.modules.base.objects.common as common

class Currency(common.Item):
    data_keys = ('name', 'symbol', 'value')
    
    def getData(self):
        sql = "SELECT name, symbol, value FROM currencies WHERE id=%s"
        params = (self.id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                self.data['name'], self.data['symbol'], \
                        self.data['value'] = results

class CurrencyObject(common.Object):
    item = Currency
    
    def dbGetAll(self):
        sql = "SELECT id FROM currencies"
        params = None
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None
    
    def dbInsert(self, name, symbol, value):
        sql = "INSERT INTO currencies (name, symbol, value) VALUES (%s, %s, %s)"
        params = (name, symbol, value)
        cursor, success = pos.db.query(sql, params)
        if success:
            _id = pos.db.conn.insert_id()
            return _id
        else:
            return None
    
    def dbUpdate(self, _id, **kwargs):
        fields = ('name', 'symbol', 'value')
        update_str = ",".join([f+"=%s" for f in fields if kwargs.has_key(f)])
        update_params = [kwargs[f] for f in fields if kwargs.has_key(f)]
        
        if len(update_str) == 0: return True
        sql = "UPDATE currencies SET "+update_str+" WHERE id=%s"
        params = update_params+[_id]
        cursor, success = pos.db.query(sql, params)
        if success:
            return True
        else:
            return None
    
    def dbDelete(self, _id):
        sql = "DELETE FROM currencies WHERE id=%s"
        params = (_id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def getDBData(self, key, val):
        if key == 'value':
            return key, float(val)
        else:
            return key, val

obj = CurrencyObject()

find = lambda _id=None, list=False, **kwargs: obj.find(list, _id, **kwargs)
add = lambda **kwargs: obj.add(**kwargs)

default = find(_id=1)

def convert(price, src_currency, dest_currency):
    s_val = float(src_currency.data['value'])
    d_val = float(dest_currency.data['value'])
    #ps*vs = pd*vd

    return float(price)*s_val/d_val
