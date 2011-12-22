import pos

import pos.modules.base.objects.common as common

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref

# TODO they are not used they should be assigned to an image of the coin or something and used to truncate to the nearest.
class CurrencyUnit(pos.database.Base, common.Item):
    __tablename__ = 'currency_units'

    id = Column(Integer, primary_key=True)
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    value = Column(Float, nullable=False)

    currency = relationship("Currency", order_by="Currency.id", backref="units")

    def __init__(self, value, currency):
        self.value = value
        self.currency = currency

    def __repr__(self):
        return "<CurrencyUnit %s>" % (self.currency.format(self.value),)

add = common.add(CurrencyUnit)
