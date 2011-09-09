import pos

import pos.modules.base.objects.common as common

class Currency(common.Item):
    data_keys = ('name', 'symbol', 'value',
                 'decimal_places', 'digit_grouping', 'format')
    
    def getData(self):
        sql = "SELECT name, symbol, value, decimal_places, digit_grouping FROM currencies WHERE id=%s"
        params = (self.id,)
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                self.data['name'], self.data['symbol'], \
                        self.data['value'], self.data['decimal_places'], \
                        self.data['digit_grouping'] = results

    def getFormatString(self):
        return (',' if self.data['digit_grouping'] else '')+\
               ('.%df' % (self.data['decimal_places'],) if self.data['decimal_places']>0 else '.0f')

    def format(self, value):
        return '%s %s' % (format(value, self.getFormatString()), self.data['symbol'])

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
    
    def dbInsert(self, name, symbol, value, decimal_places, digit_grouping):
        sql = "INSERT INTO currencies (name, symbol, value, decimal_places, digit_grouping) VALUES (%s, %s, %s, %s, %s)"
        params = (name, symbol, value, decimal_places, digit_grouping)
        cursor, success = pos.db.query(sql, params)
        if success:
            _id = pos.db.conn.insert_id()
            return _id
        else:
            return None
    
    def dbUpdate(self, _id, **kwargs):
        fields = ('name', 'symbol', 'value', 'decimal_places', 'digit_grouping')
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

    return round(float(price)*s_val/d_val, dest_currency.data['decimal_places'])
