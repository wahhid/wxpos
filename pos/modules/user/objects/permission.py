import pos

import pos.modules.base.objects.common as common

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref

permission_restriction_link = Table('permission_restriction', pos.database.Base.metadata,
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True),
    Column('restriction_id', Integer, ForeignKey('menurestrictions.id'), primary_key=True)
)

class MenuRestriction(pos.database.Base, common.Item):
    __tablename__ = "menurestrictions"
    __table_args__ = (
        UniqueConstraint('root', 'item'),
        )

    id = Column(Integer, primary_key=True)
    root = Column(String(255), nullable=False)
    item = Column(String(255), nullable=False)

    keys = ('root', 'item')
    
    #def __init__(self, root, item):
        #self.root = root
        #self.item = item

    def __repr__(self):
        return "<MenuRestriction %s.%s>" % (self.root, self.item)

class Permission(pos.database.Base, common.Item):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=False)

    menu_restrictions = relationship("MenuRestriction", secondary=permission_restriction_link, backref="permissions")

    keys = ('name', 'description', 'menu_restrictions')
    
    def __init__(self, name, description, menu_restrictions):
        self.name = name
        self.description = description
        self.menu_restrictions = menu_restrictions

    def __repr__(self):
        return "<Permission %s>" % (self.name,)

add = common.add(Permission)
