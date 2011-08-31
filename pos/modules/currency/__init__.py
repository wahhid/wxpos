import pos
from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

dependencies = ('base',)

def configDB(test=False):
    pos.db.query("""CREATE TABLE currencies (
         id int AUTO_INCREMENT PRIMARY KEY,
         name varchar(255) NOT NULL,
         symbol varchar(255) NOT NULL,
         value double NOT NULL
    )""")

    if not test: return
    
    pos.db.query("""INSERT INTO currencies (name, symbol, value) VALUES
        ('Lebanese Lira', 'L.L.', 1.0),
        ('U.S. Dollars', 'USD', 1500),
        ('Euro', 'EUR', 2000)
    """)

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu

    def loadSubItems(self):
        from pos.modules.currency.panels import CurrenciesPanel
        
        MenuItem(self.menu, "System", "Currencies", CurrenciesPanel)
