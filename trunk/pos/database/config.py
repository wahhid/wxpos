import pos

from sqlalchemy import exc
from sqlalchemy.engine.url import URL

pos.config.set_default('db', 'used', 'sqlite')

pos.config.set_default('db.sqlite', 'drivername', 'sqlite')
pos.config.set_default('db.sqlite', 'database', 'wxpos.sqlite')

pos.config.set_default('db.mysql', 'drivername', 'mysql')

pos.config.set_default('db.postgresql', 'drivername', 'postgresql')

pos.config.set_default('db.mssql', 'drivername', 'mssql')

pos.config.set_default('db.firebird', 'drivername', 'firebird')


_url = None
def loadconfig():
    config = 'db.'+pos.config['db', 'used']
    args = ('drivername', 'username', 'password', 'host', 'port', 'database', 'query')
    kwargs = dict([(a, pos.config[config, a]) for a in args if pos.config[config, a] is not None])

    global _url
    _url = URL(**kwargs)
    return _url

def clear():
    metadata = pos.database.Base.metadata
    metadata.drop_all()

def create():
    metadata = pos.database.Base.metadata
    metadata.create_all()

def use(config_name):
    pos.config['db'] = {'used': config_name}
    pos.config.save()

def get_used():
    return pos.config['db', 'used']
