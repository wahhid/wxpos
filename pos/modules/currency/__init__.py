import pos
from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

dependencies = ('base',)

def configDB(test=False):
    pos.db.query("""CREATE TABLE currencies (
         id int AUTO_INCREMENT PRIMARY KEY,
         name varchar(255) NOT NULL,
         symbol varchar(255) NOT NULL,
         value double NOT NULL,
         decimal_places INT NOT NULL DEFAULT 2,
         digit_grouping BOOL DEFAULT FALSE
    )""")

    pos.db.query("""CREATE TABLE currency_units (
         currency_id int,
         value double NOT NULL,
         FOREIGN KEY (currency_id) REFERENCES currencies(id)
    )""")

    if not test: return
    
    pos.db.query("""INSERT INTO currencies (name, symbol, value, decimal_places, digit_grouping) VALUES
        ('Lebanese Lira', 'L.L.', 1.0, 0, 1),
        ('U.S. Dollars', 'USD', 1500, 2, 1),
        ('Euro', 'EUR', 2000, 2, 1)
    """)

    pos.db.query("""INSERT INTO currency_units (currency_id, value) VALUES
        (1, 250), (1, 500), (1, 1000), (1, 5000), (1, 10000), (1, 20000), (1, 50000), (1, 100000),
        (2, 0.01), (2, 0.02), (2, 0.05), (2, 0.10), (2, 0.20), (2, 0.50), (2, 1), (2, 2), (2, 5),
            (2, 10), (2, 20), (2, 50), (2, 100),
        (3, 0.01), (3, 0.02), (3, 0.05), (3, 0.10), (3, 0.20), (3, 0.50), (3, 1), (3, 2), (3, 5),
            (3, 10), (3, 20), (3, 50), (3, 100)
    """)

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu

    def loadSubItems(self):
        from pos.modules.currency.panels import CurrenciesPanel
        
        MenuItem(self.menu, "System", "Currencies", CurrenciesPanel)
