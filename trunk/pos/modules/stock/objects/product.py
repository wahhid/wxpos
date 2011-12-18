import pos

import pos.modules.base.objects.common as common
import pos.modules.stock.objects.diary as diary

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

class Product(pos.database.Base, common.Item):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=False, default='')
    reference = Column(String(255), nullable=False, default='', unique=True)
    code = Column(String(255), nullable=False, default='', unique=True)
    price = Column(Float, nullable=False, default=0)
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    _quantity = Column('quantity', Integer, nullable=True, default=None)
    category_id = Column(Integer, ForeignKey('categories.id'))
    
    category = relationship("Category", backref="products")
    currency = relationship("Currency", backref="products")

    keys = ('name', 'description', 'reference', 'code',
             'price', 'currency', 'quantity', 'category',
             'in_stock')

    def __init__(self, name, description, reference, code, price, currency, quantity, category, in_stock=True):
        self.name = name
        self.description = description
        self.reference = reference
        self.code = code
        self.price = price
        self.currency = currency
        self._quantity = quantity if in_stock else None
        self.category = category

    def __repr__(self):
        return "<Product %s>" % (self.name,)

    @hybrid_property
    def in_stock(self):
        return self._quantity is not None

    @in_stock.setter
    def in_stock(self, value):
        if not value:
            self._quantity = None
        elif value and self._quantity is None:
            self._quantity = 0

    @in_stock.expression
    def in_stock(cls):
        return cls.quantity != None

    @hybrid_property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value
        diary.add(operation='edit', quantity=value, product=self)

    def quantity_in(self, value):
        if self._quantity is None:
            return
        self._quantity += value
        diary.add(operation='in', quantity=value, product=self)

    def quantity_out(self, value):
        if self._quantity is None:
            return
        self._quantity -= value
        diary.add(operation='out', quantity=value, product=self)

find = common.find(Product)
add = common.add(Product)
