import pos

import pos.database
import pos.modules.base.objects.common as common

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref

class TicketLine(pos.database.Base, common.Item):
    __tablename__ = 'ticketlines'

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False, default='')
    sell_price = Column(Float, nullable=False, default=0)
    amount = Column(Integer, nullable=False, default=1)
    is_edited = Column(Boolean, nullable=False, default=False)
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    
    ticket = relationship("Ticket", backref="ticketlines")
    product = relationship("Product", backref="ticketlines")

    keys = ('description', 'sell_price', 'amount',
                 'ticket', 'product', 'is_edited')

    def __init__(self, description, sell_price, amount, is_edited, ticket, product):
        self.description = description
        self.sell_price = sell_price
        self.amount = amount
        self.is_edited = is_edited
        self.ticket = ticket
        self.product = product

    def __repr__(self):
        return "<TicketLine %s in Ticket #%s>" % (self.id, self.ticket.id)

add = common.add(TicketLine)
