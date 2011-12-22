import pos

import pos.database
import pos.modules.base.objects.common as common

from pos.modules.currency.objects import currency

from pos.modules.currency.objects.currency import Currency
from pos.modules.sales.objects.ticketline import TicketLine
from pos.modules.sales.objects.ticket import Ticket

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

customer_group_link = Table('customer_group', pos.database.Base.metadata,
    Column('customer_id', Integer, ForeignKey('customers.id')),
    Column('group_id', Integer, ForeignKey('customergroups.id'))
)

class Customer(pos.database.Base, common.Item):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    code = Column(String(255), nullable=True, unique=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    max_debt = Column(Float, nullable=True)
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    comment = Column(String(255), nullable=True)

    groups = relationship("CustomerGroup", secondary=customer_group_link, backref="customers")
    currency = relationship("Currency", backref="customers")

    keys = ('name', 'code', 'first_name', 'last_name',
                 'max_debt', 'currency', 'comment', 'groups')

    def __init__(self, name, code, first_name, last_name, max_debt, currency, comment, groups):
        self.name = name
        self.code = code
        self.first_name = first_name
        self.last_name = last_name
        self.max_debt = max_debt
        self.currency = currency
        self.comment = comment
        self.groups = groups

    def __repr__(self):
        return "<Customer %s>" % (self.name)

    @hybrid_property
    def debt(self):
        session = pos.database.session()
        qry = session.query(func.sum(TicketLine.amount*TicketLine.sell_price), Currency) \
                             .filter((TicketLine.ticket_id == Ticket.id) & \
                                     (Ticket.customer == self) & \
                                     (Ticket.currency_id == Currency.id) & \
                                     (Ticket.payment_method == 'debt') & \
                                     ~Ticket.paid) \
                            .group_by(Ticket.currency_id)
        total = sum(currency.convert(c_total, c, self.currency) for c_total, c in qry.all())
        return total

add = common.add(Customer)
