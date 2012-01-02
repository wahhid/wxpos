import pos

from sqlalchemy import exc
from sqlalchemy.engine.url import URL

# Define default database configuration for different RDBMS's
pos.config.set_default('db', 'used', 'sqlite')

pos.config.set_default('db.sqlite', 'drivername', 'sqlite')
pos.config.set_default('db.sqlite', 'database', 'wxpos.sqlite')

pos.config.set_default('db.mysql', 'drivername', 'mysql')
pos.config.set_default('db.mysql', 'query', repr({'charset': 'utf8'}))

pos.config.set_default('db.postgresql', 'drivername', 'postgresql')

pos.config.set_default('db.mssql', 'drivername', 'mssql')

pos.config.set_default('db.firebird', 'drivername', 'firebird')


_url = None
def loadconfig():
    """
    Return the URL to be used with engine creation based on configuration
    """
    config = 'db.'+pos.config['db', 'used']
    args = ('drivername', 'username', 'password', 'host', 'port', 'database')
    kwargs = dict([(a, pos.config[config, a]) for a in args if pos.config[config, a] is not None])
    if pos.config[config, 'query'] is not None:
        # TODO query parameters should not be saved as repr({whatever}). use something like query.param1=value1, etc.
        kwargs['query'] = eval(pos.config[config, 'query'])

    global _url
    _url = URL(**kwargs)
    return _url

def clear():
    """
    Clear the database.
    Note: Drops all tables, does not drop database.
    """
    metadata = pos.database.Base.metadata
    metadata.drop_all()

def create():
    """
    Create the database.
    Note: Creates all the tables, does not create the database itself.
    """
    metadata = pos.database.Base.metadata
    metadata.create_all()

def use(config_name):
    """
    Change the database configuration used. 
    """
    #pos.config['db'] = {'used': config_name}
    pos.config['db', 'used'] = str(config_name)
    pos.config.save()
