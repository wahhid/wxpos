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

class find:
    def __init__(self, item):
        self.item = item

    def find(self, _id=None, list=False, **kwargs):
        # TODO remove that function from here
        raise Exception, 'object.find() should not be used anymore'
        session = pos.database.session()
        if _id is not None:
            # result = [session.query(self.item).filter_by(date_deleted=None, id=_id).one()]
            result = [session.query(self.item).filter_by(id=_id).one()]
        else:
            # result = session.query(self.item).filter_by(date_deleted=None, **kwargs).all()
            if 'closed' in kwargs:
                result = [r for r in session.query(self.item).all() if len([k for k in kwargs if getattr(r, k) != kwargs[k]]) == 0]
                print result
            else:
                result = session.query(self.item).filter_by(**kwargs).all()
        
        count = len(result)
        if list or count>1:
            return result
        elif count == 0:
            return None
        elif count == 1:
            return result[0]
    
    __call__ = find

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
