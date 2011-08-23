print '-- CONFIG INIT --'

print '*Creating database...'
import pos.db
pos.db.db = pos.db.DB()

print '*Importing modules...'
import pos.modules

def run():
    print '*Configuring database...'
    pos.modules.configDB(pos.db.db)

if __name__ == '__main__':
    run()
