import pos

import pos.modules.base.objects.common as common

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref

class Permission(pos.database.Base, common.Item):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=False)

    keys = ('name', 'description')
    
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<Permission %s>" % (self.name,)

add = common.add(Permission)
