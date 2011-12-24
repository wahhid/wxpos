from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import loadconfig

_session = None
def session():
    global _session
    if _session is None:
        _session = Session()
    return _session

engine, Base, Session = None, None, None
def init():
    global engine, Base, Session

    if engine is not None:
        return

    url = loadconfig()

    engine = create_engine(url)#, echo=True)
    Base = declarative_base(bind=engine)
    Session = sessionmaker(bind=engine)

    engine.connect()
