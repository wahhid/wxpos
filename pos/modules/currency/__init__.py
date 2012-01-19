import pos
from pos.modules import Module

class ModuleLoader(Module):
    dependencies = ('base',)
    config = [['mod.currency', {'default': ''}]]
    name = 'Multiple Currencies Support'

    def load(self):
        from pos.modules.currency.objects.currency import Currency
        from pos.modules.currency.objects.currencyunit import CurrencyUnit
        return [Currency, CurrencyUnit]

    def test(self):
        from pos.modules.currency.objects.currency import Currency
        from pos.modules.currency.objects.currencyunit import CurrencyUnit
        
        LL = Currency(name='Lebanese Lira', symbol='L.L.', value=1.0, decimal_places=0, digit_grouping=True)
        USD = Currency(name='U.S. Dollar', symbol='USD', value=1500, decimal_places=2, digit_grouping=True)
        EUR = Currency(name='Euro', symbol='EUR', value=2000, decimal_places=2, digit_grouping=True)
    
        ll_values = [250, 500, 1000, 5000, 10000, 20000, 50000, 100000]
        usd_values = [0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1, 2, 5, 10, 20, 50, 100]
        eur_values = [0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1, 2, 5, 20, 20, 50, 100, 500]
    
        [CurrencyUnit(value=v, currency=LL) for v in ll_values]
        [CurrencyUnit(value=v, currency=USD) for v in usd_values]
        [CurrencyUnit(value=v, currency=EUR) for v in eur_values]
    
        session = pos.database.session()
        session.add(LL)
        session.add(USD)
        session.add(EUR)
        session.commit()

    def menu(self):
        from pos.modules.currency.panels import CurrenciesPanel
            
        return [[],
                [{'parent': 'System', 'label': 'Currencies', 'page': CurrenciesPanel}]]

    def init(self):
        import wx
        from pos.modules.currency.dialogs import CurrencyDialog
        from pos.modules.currency.objects.currency import Currency
        
        session = pos.database.session()
        currency_count = session.query(Currency).count()
        if currency_count == 0:
            dlg = CurrencyDialog(None)
            result = dlg.ShowModal()
            if result == wx.ID_OK:
                c = Currency(**dlg.data)
                session.add(c)
                session.commit()
                return c
            else:
                return False
    
    def config_panels(self):
        from pos.modules.currency.panels import CurrencyConfigPanel 
        return [CurrencyConfigPanel]
