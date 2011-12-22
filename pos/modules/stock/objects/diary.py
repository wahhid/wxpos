import pos

import pos.modules.base.objects.common as common

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, Enum, DateTime, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

class DiaryEntry(pos.database.Base, common.Item):
    __tablename__ = 'stockdiary'

    id = Column(Integer, primary_key=True)
    operation = Column(Enum('in', 'out', 'edit'), nullable=False)
    quantity = Column(Integer, nullable=True)
    date = Column(DateTime, nullable=False, default=func.current_timestamp())
    product_id = Column(Integer, ForeignKey('products.id'))
    
    product = relationship("Product", backref="diaryentries")

    keys = ('operation', 'quantity', 'date', 'product')

    def __init__(self, operation, quantity, product):
        self.operation = operation
        self.quantity = quantity
        self.product = product

    def __repr__(self):
        return "<DiaryEntry %d %s of %s on %s>" % \
               (self.quantity, self.operation, self.product, self.date)

add = common.add(DiaryEntry)
