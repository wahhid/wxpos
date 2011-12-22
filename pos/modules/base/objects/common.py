import pos.database
import warnings

#from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, Enum, DateTime, MetaData, ForeignKey
#from sqlalchemy.orm import relationship, backref

class Item:

    # TODO arrange soft deletions to have 3 tables (or more) one mother(id only), one active children, one deleted children
    #        see bookmark "The trouble with soft delete"
    #date_deleted = Column(DateTime, nullable=True, default=None)
    
    # TODO I thought the keys dict in every Item subclass made sense but it is useless
    #        should make sure before removing it from everywhere
    def fillDict(self, D):
        for k in D.keys():
            D[k] = getattr(self, k)

    def update(self, **kwargs):
        session = pos.database.session()
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        session.commit()
        return True

    def delete(self):
        session = pos.database.session()
        session.delete(self)
        # TODO check the soft delete thingy
        #session.date_deleted = func.now()
        session.commit()
        return True

class add:
    def __init__(self, item):
        self.item = item

    def add(self, **kwargs):
        i = self.item(**kwargs)
        session = pos.database.session()
        session.add(i)
        session.commit()
        return i

    __call__ = add
