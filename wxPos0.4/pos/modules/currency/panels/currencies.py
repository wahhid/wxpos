import wx

from pos.modules.base.objects.idManager import ids

import pos.modules.currency.objects.currency as currency

from pos.modules.base.panels import ManagePanel

class CurrenciesPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, ids['currenciesPanel'],
                style=wx.TAB_TRAVERSAL)
        
        self._init_panel('Currencies', DataValidator)
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Symbol', wx.TextCtrl, 'symbol', '')
        self.createField('Value', wx.TextCtrl, 'value', '')
        self._init_fields()

    getItems = lambda self: [{'text': c.data['name']} for c in currency.find(list=True)]
    getItem = lambda self, item: currency.find(name=item.GetText())
    newItem = lambda self: currency.add(**self.data)
    updateItem = lambda self, c: c.update(**self.data)
    canEditItem = lambda self, c: True
    canDeleteItem = lambda self, c: False
    
    def fillData(self):
        c = self.getCurrentItem()
        if c is None: return
        self.data = c.data.copy()
    
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
            if len(data) == 0:
                return False
            if self.key == 'value':
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
            if self.key in ('name', 'symbol'):
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
        if self.key in ('name', 'symbol', 'value'):
            data = win.GetValue()
        return data
                
