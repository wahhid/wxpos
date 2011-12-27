import pos
from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey

dependencies = ('base',)

pos.config.set_default('mod.currency', 'default', None)

def load_database_objects():
    from pos.modules.currency.objects.currency import Currency
    from pos.modules.currency.objects.currencyunit import CurrencyUnit

def test_database_values():
    from pos.modules.currency.objects.currency import Currency
    from pos.modules.currency.objects.currencyunit import CurrencyUnit
    
    LL = Currency('Lebanese Lira', 'L.L.', 1.0, 0, True)
    USD = Currency('U.S. Dollar', 'USD', 1500, 2, True)
    EUR = Currency('Euro', 'EUR', 2000, 2, True)

    ll_values = [250, 500, 1000, 5000, 10000, 20000, 50000, 100000]
    usd_values = [0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1, 2, 5, 10, 20, 50, 100]
    eur_values = [0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1, 2, 5, 20, 20, 50, 100, 500]

    [CurrencyUnit(v, LL) for v in ll_values]
    [CurrencyUnit(v, USD) for v in usd_values]
    [CurrencyUnit(v, EUR) for v in eur_values]

    session = pos.database.session()
    session.add(LL)
    session.add(USD)
    session.add(EUR)
    session.commit()

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu

    def loadSubItems(self):
        from pos.modules.currency.panels import CurrenciesPanel
        
        MenuItem(self.menu, "System", "Currencies", CurrenciesPanel)
