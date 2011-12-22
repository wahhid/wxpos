import pos

import pos.modules.base.objects.common as common

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

role_permission_link = Table('role_permission', pos.database.Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

class Role(pos.database.Base, common.Item):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    permissions = relationship("Permission", secondary=role_permission_link, backref="roles")

    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions

    def isPermitted(self, permission):
        if permission is None:
            return True
        elif type(permission) == str:
            return (permission in [p.name for p in self.permissions])
        else:
            return (permission in self.permissions)

    def __repr__(self):
        return "<Role %s>" % (self.name,)

add = common.add(Role)
