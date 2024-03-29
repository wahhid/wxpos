import pos

import pos.modules.base.objects.common as common

from pos.modules.stock.objects.product import Product
from pos.modules.sales.objects.ticketline import TicketLine

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, Enum, DateTime, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

class Ticket(pos.database.Base, common.Item):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    date_open = Column(DateTime, nullable=True, default=func.current_timestamp())
    date_close = Column(DateTime, nullable=True)
    payment_method = Column(Enum('cash', 'cheque', 'voucher', 'card', 'free', 'debt', name="payment_method_enum"), nullable=True)
    date_paid = Column(DateTime, nullable=True)
    comment = Column(String(255), nullable=True)
    discount = Column(Float, nullable=False, default=0)
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    currency = relationship("Currency", backref="tickets")
    customer = relationship("Customer", backref="tickets")
    user = relationship("User", backref="tickets")

    @hybrid_property
    def paid(self):
        return self.date_paid is not None

    @paid.setter
    def paid(self, value):
        if value:
            self.date_paid = func.now()
        else:
            self.date_paid = None

    @paid.expression
    def paid(cls):
        return cls.date_paid != None

    def pay(self, method, paid=True):
        self.payment_method = method
        self.paid = paid
        session = pos.database.session()
        session.commit()
    
    @hybrid_property
    def closed(self):
        return self.date_close is not None

    @closed.setter
    def closed(self, value):
        if value:
            self.date_close = func.now()
            session = pos.database.session()
            result = session.query(Product, TicketLine.amount).filter((TicketLine.ticket == self) & \
                                                        (TicketLine.product_id == Product.id) & \
                                                        Product.in_stock).all()
            for p, amount in result:
                p.quantity_out(amount)
            session.commit()
        else:
            self.date_close = None

    @closed.expression
    def closed(cls):
        return cls.date_close != None

    @hybrid_property
    def total(self):
        session = pos.database.session()
        total = session.query(func.sum(TicketLine.total)).filter(TicketLine.ticket == self).one()[0]
        return total*(1-self.discount) if total is not None else 0
    
    @hybrid_property
    def display(self):
        # TODO see if it is a good idea to use another way to number tickets..
        """
        base_36 = str_base(self.id, 36).upper()
        display = ''
        sep = 3
        format_str = '{:0>'+str(sep)+'}'
        for i in range(len(base_36), 0, -sep):
            display = format_str.format(base_36[max(0, i-sep):i])+'-'+display
        display = display[:-1] if len(display)>0 else ''
        return '#'+display
        """
        return '#%d' % (self.id,)
    
    @display.expression
    def display(self):
        return func.concat('#', self.id)
    
    def __repr__(self):
        return "<Ticket %s>" % (self.id,)

def digit_to_char(digit):
    if digit < 10: return chr(ord('0') + digit)
    else: return chr(ord('a') + digit - 10)

def str_base(number,base):
    if number < 0:
        return '-' + str_base(-number,base)
    else:
        (d,m) = divmod(number,base)
        if d:
            return str_base(d,base) + digit_to_char(m)
        else:
            return digit_to_char(m)
