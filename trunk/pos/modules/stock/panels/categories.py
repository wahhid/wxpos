import wx

import pos

import pos.modules.stock.objects.category as category
from pos.modules.stock.objects.category import Category
from pos.modules.stock.objects.product import Product

from pos.modules.base.panels import ManagePanel

class CategoriesPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)
        
        self._init_panel('Categories', DataValidator)
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Parent Category', wx.Choice, 'parent', None)
        self._init_fields()

    getItems = lambda self: pos.database.session().query(Category, Category.name).all()
    newItem = lambda self: category.add(**self.data)
    updateItem = lambda self, c: c.update(**self.data)
    canEditItem = lambda self, c: True
    
    def canDeleteItem(self, c):
        session = pos.database.session()
        category_count = session.query(Category).filter(Category.parent == c).count()
        product_count = session.query(Product).filter(Product.category == c).count()
        return (category_count == 0 and product_count == 0)
    
    def fillData(self):
        session = pos.database.session()
        c = self.getCurrentItem()
        if c is None:
            category_choices = session.query(Category.name).all()
        else:
            category_choices = session.query(Category.name).filter(Category.id != c.id).all()
        self.getField('parent').SetItems(['[None]']+[c[0] for c in category_choices])
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
            if self.key == 'name':
                if len(data) == 0:
                    return False
            elif self.key == 'parent':
                return True
        except:
            print '-- ERROR -- in DataValidator.TransferToWindow'
            print '--', self.key, self.panel.data
            raise
        return True

    def TransferToWindow(self):
        try:
            win = self.GetWindow()
            data = self.panel.data[self.key]
            if self.key == 'name':
                win.SetValue(data)
            elif self.key == 'parent':
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
            data = self.getData(win)
            self.panel.data[self.key] = data
        except:
            print '-- ERROR -- in DataValidator.TransferFromWindow'
            print '--', self.key, self.panel.data
            raise
        return True
        
    def getData(self, win):
        data = None
        if self.key == 'name':
            data = win.GetValue()
        elif self.key == 'parent':
            index = win.GetSelection()
            if index>0:
                category_name = win.GetStringSelection()
                session = pos.database.session()
                data = session.query(Category).filter_by(name=category_name).one()
            else:
                data = None
        return data
                
