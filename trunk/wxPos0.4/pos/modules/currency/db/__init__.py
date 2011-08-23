from pos.db.subset import DBSubset

from .currency import CurrencyDB

class ModuleDB(DBSubset, CurrencyDB):
    pass

def config(db):
    db.createTable("currencies", """
         id int AUTO_INCREMENT PRIMARY KEY,
         name varchar(255) NOT NULL,
         symbol varchar(255) NOT NULL,
         value double NOT NULL
    """)

    db.query("currency.db.config", """INSERT INTO currencies (name, symbol, value) VALUES
        ('Lebanese Lira', 'L.L.', 1.0),
        ('U.S. Dollars', 'USD', 1500),
        ('Euro', 'EUR', 2000)
    """)
