
def init():
    import wx
    import pos
    from .dialogs import CurrencyDialog
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