import wx

from pos.modules.base.objects.idManager import ids

import pos.modules.currency.objects.currency as currency

import pos.modules.stock.objects.product as product
import pos.modules.stock.objects.category as category

from pos.modules.base.panels import ManagePanel

class ProductsPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, id=ids['productsPanel'], parent=parent, style=wx.TAB_TRAVERSAL)
        
        self._init_panel('Products', DataValidator)
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Description', wx.TextCtrl, 'description', '')
        self.createField('Reference', wx.TextCtrl, 'reference', '')
        self.createField('Code', wx.TextCtrl, 'code', '')
        self.createField('Price', wx.TextCtrl, 'price', '')
        self.createField('Currency', wx.Choice, 'currency', currency.default)
        self.createField('Quantity', wx.SpinCtrl, 'quantity', 0,
                         value='0', style=wx.SP_ARROW_KEYS, min=0)
        self.createField('In Stock', wx.CheckBox, 'in_stock', True)
        self.createField('Category', wx.Choice, 'category', None)
        self._init_fields()

    getItems = lambda self: [{'text': p.data['name']} for p in product.find(list=True)]
    getItem = lambda self, item: product.find(name=item.GetText())
    newItem = lambda self: product.add(**self.data)
    updateItem = lambda self, p: p.update(**self.data)
    canEditItem = lambda self, p: True
    canDeleteItem = lambda self, p: True
    
    def fillData(self):
        category_choices = map(lambda c: c.data['name'], category.find(list=True))
        choices = ['[None]']+category_choices
        self.getField('category').SetItems(choices)
        
        currency_choices = map(lambda c: c.data['symbol'], currency.find(list=True))
        self.getField('currency').SetItems(currency_choices)

        self.getField('quantity').Enable(False)
        p = self.getCurrentItem()
        if p is None: return
        self.data = p.data.copy()

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
                win.SetStringSelection(data.data['symbol'])
            elif self.key == 'category':
                if data is None:
                    win.SetSelection(0)
                else:
                    win.SetStringSelection(data.data['name'])
        except:
            print '-- ERROR -- in DataValidator.TransferToWindow'
            print '--', self.key, self.panel.data
            raise
        return True

    def TransferFromWindow(self):
        try:
            win = self.GetWindow()
            if self.key in ('name', 'description', 'reference', 'code', 'price', 'quantity'):
                data = win.GetValue()
            elif self.key == 'in_stock':
                data = win.GetValue()
            elif self.key == 'currency':
                currency_symbol = win.GetStringSelection()
                data = currency.find(symbol=currency_symbol)
            elif self.key == 'category':
                index = win.GetSelection()
                if index>0:
                    category_name = win.GetStringSelection()
                    data = category.find(name=category_name)
                else:
                    data = None
            self.panel.data[self.key] = data
        except:
            print '-- ERROR -- in DataValidator.TransferFromWindow'
            print '--', self.key, self.panel.data
            raise
        return True
