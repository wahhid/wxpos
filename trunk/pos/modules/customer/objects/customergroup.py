import pos

import pos.database
import pos.modules.base.objects.common as common

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref

class CustomerGroup(pos.database.Base, common.Item):
    __tablename__ = 'customergroups'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    comment = Column(String(255), nullable=True)
    
    keys = ('name', 'comment')

    def __init__(self, name, comment):
        self.name = name
        self.comment = comment

    def __repr__(self):
        return "<CustomerGroup %s>" % (self.name)

add = common.add(CustomerGroup)
