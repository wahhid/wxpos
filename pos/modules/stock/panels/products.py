import wx
import sys

import pos

import pos.modules.currency.objects.currency as currency
from pos.modules.currency.objects.currency import Currency
from pos.modules.stock.objects.product import Product
from pos.modules.stock.objects.category import Category

from pos.modules.base.panels import ManagePanel
from pos.modules.base.objects import validator as base_validator
from pos.modules.base.objects.formatter import TextFormatter, AlphaNumericFormatter, FloatFormatter

class ProductsPanel(ManagePanel):
    def __init__(self, parent):
        ManagePanel.__init__(self, parent, -1, 'Products', Product, DataValidator)
        
        self.createField('Name', wx.TextCtrl, 'name', '', formatter=TextFormatter(required=True))
        self.createField('Description', wx.TextCtrl, 'description', '', formatter=TextFormatter(required=False))
        self.createField('Reference', wx.TextCtrl, 'reference', '', formatter=AlphaNumericFormatter(required=False))
        self.createField('Code', wx.TextCtrl, 'code', '', formatter=AlphaNumericFormatter(required=False))
        self.createField('Price', wx.TextCtrl, 'price', '', formatter=FloatFormatter(required=True))
        self.createField('Currency', wx.Choice, 'currency', currency.get_default())
        self.createField('Quantity', wx.SpinCtrl, 'quantity', 0,
                         value='0', min=0, max=sys.maxint, style=wx.SP_ARROW_KEYS)
        self.createField('In Stock', wx.CheckBox, 'in_stock', True)
        self.getField('in_stock').Bind(wx.EVT_CHECKBOX, self.OnInStockCheckBox)
        self.createField('Category', wx.Choice, 'category', None)
        self._init_fields()

    canEditItem = lambda self, p: True
    canDeleteItem = lambda self, p: True
    
    def OnInStockCheckBox(self, event):
        event.Skip()
        in_stock = self.getField('in_stock').IsChecked()
        self.getField('quantity').Enable(in_stock)

class DataValidator(base_validator.BaseValidator):
    def GetWindowData(self):
        win = self.GetWindow()
        if self.key in ('name', 'description', 'price'):
            return win.GetValue()
        elif self.key in ('reference', 'code'):
            data = win.GetValue()
            if data == '':
                return None
            return data
        elif self.key == 'quantity':
            if not self.panel.getField('in_stock').IsChecked():
                return None
            return win.GetValue()
        elif self.key == 'in_stock':
            return win.GetValue()
        elif self.key == 'currency':
            currency_symbol = win.GetStringSelection()
            session = pos.database.session()
            return session.query(Currency).filter_by(symbol=currency_symbol).one()
        elif self.key == 'category':
            index = win.GetSelection()
            if index>0:
                category_name = win.GetStringSelection()
                session = pos.database.session()
                return session.query(Category).filter_by(name=category_name).one()
            else:
                return None
    
    def ValidateWindowData(self, data):
        return True
    
    def SetWindowData(self, data):
        win = self.GetWindow()
        if self.key in ('name', 'description'):
            win.SetValue(data)
        elif self.key in ('reference', 'code'):
            if data is None:
                win.SetValue('')
            else:
                win.SetValue(data)
        elif self.key == 'price':
            win.SetValue(str(data))
        elif self.key == 'quantity':
            editing = self.panel.IsEnabled()
            win.Enable(editing and self.panel.data['in_stock'])
            if data is None:
                win.SetValue(0)
            else:
                win.SetValue(data)
        elif self.key == 'in_stock':
            win.SetValue(data)
        elif self.key == 'currency':
            session = pos.database.session()
            currency_choices = session.query(Currency.symbol).all()
            win.SetItems([c[0] for c in currency_choices])
            if data is None:
                win.SetSelection(-1)
            else:
                win.SetStringSelection(data.symbol)
        elif self.key == 'category':
            session = pos.database.session()
            category_choices = session.query(Category.display).all()
            self.panel.getField('category').SetItems(['[None]']+[c[0] for c in category_choices])
            if data is None:
                win.SetSelection(0)
            else:
                win.SetStringSelection(data.name)
