import pos

from sqlalchemy import exc
from sqlalchemy.engine.url import URL

_url = None
def loadconfig():
    if not pos.config.has_section('db'):
        setdefault()
    config = 'db.'+pos.config.get('db', 'used')
    args = ('drivername', 'username', 'password', 'host', 'port', 'database', 'query')
    kwargs = dict([(a, pos.config.get(config, a)) for a in args if pos.config.has_option(config, a)])

    global _url
    _url = URL(**kwargs)
    return _url

def setdefault():
    for section in pos.config.sections():
        if section.startswith('db.'):
            pos.config.remove_section(section)
    pos.config.add_section('db')
    pos.config.set('db', 'used', 'sqlite')
    pos.config.add_section('db.sqlite')
    pos.config.set('db.sqlite', 'drivername', 'sqlite')
    pos.saveConfig()

def clear():
    metadata = pos.database.Base.metadata
    metadata.drop_all()

def create():
    metadata = pos.database.Base.metadata
    metadata.create_all()

def use(config_name):
    if not pos.config.has_section('db'):
        setdefault()
    pos.config.set('db', 'used', config_name)
    pos.saveConfig()

def get_used():
    if not pos.config.has_section('db'):
        setdefault()
    return pos.config.get('db', 'used')
