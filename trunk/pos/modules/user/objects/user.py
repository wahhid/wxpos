import pos

import pos.modules.base.objects.common as common

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

from md5 import md5

def encode(password):
    return md5(password).hexdigest()

class User(pos.database.Base, common.Item):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    encoded_password = Column('password', String(32), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship('Role', order_by="Role.id", backref="users")

    keys = ('username', 'password', 'role')

    def __init__(self, username, password, role):
        self.username = username
        self.encoded_password = encode(password)
        self.role = role

    @hybrid_property
    def password(self):
        return self.encoded_password

    @password.setter
    def password(self, value):
        self.encoded_password = encode(value)

    def login(self, password):
        return self.encoded_password == encode(password)

    def __repr__(self):
        return "<User %s>" % (self.username,)

add = common.add(User)

current = None
