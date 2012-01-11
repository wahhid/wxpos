import wx

import pos

from pos.modules.currency.objects.currency import Currency

class ModuleConfigPanel(wx.Panel):
    label = 'Currency'
    
    def _init_sizers(self):
        self.mainSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.mainSizer.Add(self.defaultLbl, 0)
        self.mainSizer.Add(self.defaultChoice, 0, border=10, flag=wx.LEFT)

        self.SetSizer(self.mainSizer)

    def _init_main(self):
        self.defaultLbl = wx.StaticText(self, -1, label='Default Currency')
        self.defaultChoice = wx.Choice(self, -1)
        self.defaultChoice.SetValidator(DataValidator(self, 'default'))
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)

        self._init_main()
        self._init_sizers()
        self.data = {}

        self.updateCurrencyList()

    def updateCurrencyList(self):
        session = pos.database.session()
        currency_names = session.query(Currency.name).all()
        self.defaultChoice.SetItems([c[0] for c in currency_names])

class DataValidator(wx.PyValidator):
    def __init__(self, panel, key):
        wx.PyValidator.__init__(self)
        self.panel = panel
        self.key = key

    Clone = lambda self: DataValidator(self.panel, self.key)

    def Validate(self, parent):
        return True

    def TransferToWindow(self):
        win = self.GetWindow()
        if self.key == 'default':
            currency_id = pos.config['mod.currency', 'default']
            if currency_id != '':
                session = pos.database.session()
                currency_name = session.query(Currency.name).filter_by(id=currency_id).one()[0]
                win.SetStringSelection(currency_name)
            else:
                win.SetSelection(-1)
        return True

    def TransferFromWindow(self):
        win = self.GetWindow()
        if self.key == 'default':
            session = pos.database.session()
            data = str(session.query(Currency.id).filter_by(name=win.GetStringSelection()).one()[0])
        self.panel.data[self.key] = data
        return True
