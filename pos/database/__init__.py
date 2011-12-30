from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import loadconfig

_session = None
def session():
    """
    Returns a new session if none is present.
    TODO It is almost useless as it is always the same session that is returned. Check SQLAlchemy documentation in ORM>Session>FAQ for when to create a session.
    """
    global _session
    if _session is None:
        _session = Session()
    return _session

engine, Base, Session = None, None, None
def init():
    """
    Creates the SQLAlchemy engine, Session class and declarative base using the user's configuration.
    """
    global engine, Base, Session

    if engine is not None:
        return

    url = loadconfig()

    engine = create_engine(url)#, echo=True)
    Base = declarative_base(bind=engine)
    Session = sessionmaker(bind=engine)

    # This is called to ensure an error is raised if connection failed
    engine.connect()
