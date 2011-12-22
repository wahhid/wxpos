import wx

import pos

from pos.modules.currency.objects.currency import Currency

from pos.modules.base.panels import ManagePanel

class CurrenciesPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)
        
        self._init_panel('Currencies', DataValidator)
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Symbol', wx.TextCtrl, 'symbol', '')
        self.createField('Value', wx.TextCtrl, 'value', '')
        self.createField('Decimal Places', wx.SpinCtrl, 'decimal_places', 0)
        self.createField('Digit Grouping', wx.CheckBox, 'digit_grouping', True)
        self._init_fields()

    getItems = lambda self: pos.database.session().query(Currency, Currency.name).all()
    newItem = lambda self: currency.add(**self.data)
    updateItem = lambda self, c: c.update(**self.data)
    canEditItem = lambda self, c: True
    canDeleteItem = lambda self, c: True
    
    def fillData(self):
        c = self.getCurrentItem()
        if c is None: return
        c.fillDict(self.data)
    
class DataValidator(wx.PyValidator):
    def __init__(self, panel, key):
        wx.PyValidator.__init__(self)
        self.panel = panel
        self.key = key

    Clone = lambda self: DataValidator(self.panel, self.key)

    def Validate(self, parent):
        try:
            win = self.GetWindow()
            data = self.getData(win)
            if self.key in ('name', 'symbol'):
                return len(data)>0
            elif self.key == 'decimal_places':
                return True
            elif self.key == 'digit_grouping':
                return True
            elif self.key == 'value':
                try:
                    float(data)
                except:
                    return False
        except:
            print '-- ERROR -- in DataValidator.TransferToWindow'
            print '--', self.key, self.panel.data
            raise
        return True

    def TransferToWindow(self):
        try:
            win = self.GetWindow()
            data = self.panel.data[self.key]
            if self.key in ('name', 'symbol', 'decimal_places', 'digit_grouping'):
                win.SetValue(data)
            elif self.key == 'value':
                win.SetValue(str(data))
        except:
            print '-- ERROR -- in DataValidator.TransferToWindow'
            print '--', self.key, self.panel.data
            raise
        return True

    def TransferFromWindow(self):
        try:
            win = self.GetWindow()
            data = self.getData(win)
            self.panel.data[self.key] = data
        except:
            print '-- ERROR -- in DataValidator.TransferFromWindow'
            print '--', self.key, self.panel.data
            raise
        return True
        
    def getData(self, win):
        data = None
        if self.key in ('name', 'symbol', 'value', 'decimal_places', 'digit_grouping'):
            data = win.GetValue()
        return data
                