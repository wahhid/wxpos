import pos

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey

#from sqlalchemy import event, exc

url = None
def loadconfig():
    global url
    default_config = {'hostname': '', 'port': '',
              'username': '', 'password': '',
              'db_name': ''}

    if not pos.config.has_section('MySQL'):
        pos.config.add_section('MySQL')

    host = pos.config.get('MySQL', 'hostname')
    port = pos.config.get('MySQL', 'port')
    username = pos.config.get('MySQL', 'username')
    password = pos.config.get('MySQL', 'password')
    db_name = pos.config.get('MySQL', 'db_name')

    url = URL('mysql', username=username,
              password=password,
              host=host,
              #port=port,
              database=db_name)

def clear():
    metadata = Base.metadata
    metadata.drop_all()

def create():
    metadata = Base.metadata
    metadata.create_all()

_session = None
def session():
    global _session
    if _session is None:
        _session = Session()
    return _session

#def on_connect(dbapi_con, connection_record):
#    print "New DBAPI connection:", dbapi_con

engine, Base, Session = None, None, None
def init():
    global engine, Base, Session

    loadconfig()

    engine = create_engine(url)#, echo=True)
    Base = declarative_base(bind=engine)
    Session = sessionmaker(bind=engine)

    #event.listen(engine, 'first_connect', on_first_connect)
    #event.listen(engine, 'connect', on_connect)

def restart():
    loadconfig()

    global _session
    del _session
    _session = None
    
    global engine, Base, Session

    del engine
    engine = create_engine(url)
    Base.bind = engine
    Session.bind = engine
