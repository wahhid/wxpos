import wx

import pos

import pos.modules.currency.objects.currency as currency
from pos.modules.currency.objects.currency import Currency
import pos.modules.stock.objects.product as product
from pos.modules.stock.objects.product import Product
from pos.modules.stock.objects.category import Category

from pos.modules.base.panels import ManagePanel

class ProductsPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)
        
        self._init_panel('Products', DataValidator)
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Description', wx.TextCtrl, 'description', '')
        self.createField('Reference', wx.TextCtrl, 'reference', '')
        self.createField('Code', wx.TextCtrl, 'code', '')
        self.createField('Price', wx.TextCtrl, 'price', '')
        self.createField('Currency', wx.Choice, 'currency', currency.get_default())
        self.createField('Quantity', wx.SpinCtrl, 'quantity', 0,
                         value='0', style=wx.SP_ARROW_KEYS)
        self.createField('In Stock', wx.CheckBox, 'in_stock', True)
        self.createField('Category', wx.Choice, 'category', None)
        self._init_fields()
        
        self.getField('in_stock').Bind(wx.EVT_CHECKBOX, self.OnInStockCheckBox)

    getItems = lambda self: pos.database.session().query(Product, Product.name).all()
    newItem = lambda self: product.add(**self.data)
    updateItem = lambda self, p: p.update(**self.data)
    canEditItem = lambda self, p: True
    canDeleteItem = lambda self, p: True
    
    def fillData(self):
        session = pos.database.session()
        category_choices = session.query(Category.name).all()
        self.getField('category').SetItems(['[None]']+[c[0] for c in category_choices])
        
        currency_choices = session.query(Currency.symbol).all()
        self.getField('currency').SetItems([c[0] for c in currency_choices])

        p = self.getCurrentItem()
        editing = self.getField('name').IsEnabled()
        if p is None:
            self.getField('quantity').Enable(editing and self.data['in_stock'])
        else:
            self.getField('quantity').Enable(editing and p.in_stock)
        if p is None: return
        p.fillDict(self.data)
    
    def OnInStockCheckBox(self, event):
        event.Skip()
        in_stock = self.getField('in_stock').IsChecked()
        self.getField('quantity').Enable(in_stock)

class DataValidator(wx.PyValidator):
    def __init__(self, panel, key):
        wx.PyValidator.__init__(self)
        self.panel = panel
        self.key = key

    Clone = lambda self: DataValidator(self.panel, self.key)

    def Validate(self, parent):
        win = self.GetWindow()
        return True

    def TransferToWindow(self):
        try:
            win = self.GetWindow()
            data = self.panel.data[self.key]
            if self.key in ('name', 'description', 'reference', 'code'):
                win.SetValue(data)
            elif self.key == 'price':
                win.SetValue(str(data))
            elif self.key == 'quantity':
                if data is None:
                    win.SetValue(0)
                else:
                    win.SetValue(data)
            elif self.key == 'in_stock':
                win.SetValue(data)
            elif self.key == 'currency':
                if data is not None:
                    win.SetStringSelection(data.symbol)
            elif self.key == 'category':
                if data is None:
                    win.SetSelection(0)
                else:
                    win.SetStringSelection(data.name)
        except:
            print '-- ERROR -- in DataValidator.TransferToWindow'
            print '--', self.key, self.panel.data
            raise
        return True

    def TransferFromWindow(self):
        try:
            win = self.GetWindow()
            if self.key in ('name', 'description', 'reference', 'code', 'price'):
                data = win.GetValue()
            elif self.key == 'quantity':
                data = win.GetValue()
                if not self.panel.getField('in_stock').IsChecked():
                    data = None
            elif self.key == 'in_stock':
                data = win.GetValue()
            elif self.key == 'currency':
                currency_symbol = win.GetStringSelection()
                session = pos.database.session()
                data = session.query(Currency).filter_by(symbol=currency_symbol).one()
            elif self.key == 'category':
                index = win.GetSelection()
                if index>0:
                    category_name = win.GetStringSelection()
                    session = pos.database.session()
                    data = session.query(Category).filter_by(name=category_name).one()
                else:
                    data = None
            self.panel.data[self.key] = data
        except:
            print '-- ERROR -- in DataValidator.TransferFromWindow'
            print '--', self.key, self.panel.data
            raise
        return True
