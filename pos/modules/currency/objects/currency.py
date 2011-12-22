import pos

import pos.modules.base.objects.common as common

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref

class Currency(pos.database.Base, common.Item):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    symbol = Column(String(5), nullable=False, unique=True)
    value = Column(Float, nullable=False)
    decimal_places = Column(Integer, nullable=False, default=2)
    digit_grouping = Column(Boolean, default=False)

    keys = ('name', 'symbol', 'value',
                 'decimal_places', 'digit_grouping')

    def __init__(self, name, symbol, value, decimal_places, digit_grouping):
        self.name = name
        self.symbol = symbol
        self.value = value
        self.decimal_places = decimal_places
        self.digit_grouping = digit_grouping

    def __repr__(self):
        return "<Currency %s>" % (self.symbol,)

    def getFormatString(self):
        return (',' if self.digit_grouping else '')+\
               ('.%df' % (max(0, self.decimal_places),))

    def format(self, value):
        return '%s %s' % (format(round(value, max(0, self.decimal_places)), self.getFormatString()), self.symbol)

add = common.add(Currency)

def get_default():
    # TODO integrate it with a system that allows the user to change the default currency
    session = pos.database.session()
    return session.query(Currency).first()

def convert(price, src_currency, dest_currency):
    s_val = float(src_currency.value)
    d_val = float(dest_currency.value)
    #ps*vs = pd*vd

    return float(price)*s_val/d_val
    #return round(float(price)*s_val/d_val, dest_currency.decimal_places)
