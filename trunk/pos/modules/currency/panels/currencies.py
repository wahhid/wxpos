import wx
import sys

import pos

from pos.modules.currency.objects.currency import Currency

from pos.modules.base.panels import ManagePanel
from pos.modules.base.objects import validator as base_validator
from pos.modules.base.objects.formatter import FloatFormatter

class CurrenciesPanel(ManagePanel):
    def __init__(self, parent):
        ManagePanel.__init__(self, parent, -1, 'Currencies', Currency, DataValidator)
        
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Symbol', wx.TextCtrl, 'symbol', '')
        self.createField('Value', wx.SpinCtrl, 'value', 0, formatter=FloatFormatter(required=True),
                         min=0, max=sys.maxint)
        self.createField('Decimal Places', wx.SpinCtrl, 'decimal_places', 0)
        self.createField('Digit Grouping', wx.CheckBox, 'digit_grouping', True)
        self._init_fields()

    canEditItem = lambda self, c: True
    canDeleteItem = lambda self, c: True

class DataValidator(base_validator.BaseValidator):
    def GetWindowData(self):
        win = self.GetWindow()
        if self.key in ('name', 'symbol', 'value', 'decimal_places', 'digit_grouping'):
            return win.GetValue()
    
    def ValidateWindowData(self, data):
        return True
    
    def SetWindowData(self, data):
        win = self.GetWindow()
        if self.key in ('name', 'symbol', 'value', 'decimal_places', 'digit_grouping'):
            win.SetValue(data)
