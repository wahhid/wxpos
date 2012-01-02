import wx

import pos

from pos.modules.stock.objects.category import Category
from pos.modules.stock.objects.product import Product

from pos.modules.base.panels import ManagePanel
from pos.modules.base.objects import validator as base_validator
from pos.modules.base.objects.formatter import TextFormatter

class CategoriesPanel(ManagePanel):
    def __init__(self, parent):
        ManagePanel.__init__(self, parent, -1, 'Categories', Category, DataValidator)
        
        self.createField('Name', wx.TextCtrl, 'name', '', formatter=TextFormatter(required=True))
        self.createField('Parent Category', wx.Choice, 'parent', None)
        self._init_fields()

    canEditItem = lambda self, c: True    
    def canDeleteItem(self, c):
        session = pos.database.session()
        category_count = session.query(Category).filter(Category.parent == c).count()
        product_count = session.query(Product).filter(Product.category == c).count()
        return (category_count == 0 and product_count == 0)
    
    def fillForm(self):
        item = self.getCurrentItem()
        session = pos.database.session()
        if item is None:
            category_choices = session.query(Category.display).all()
        else:
            category_choices = session.query(Category.display).filter(Category.id != c.id).all()
        self.getField('parent').SetItems(['[None]']+[c[0] for c in category_choices])
        ManagePanel.fillForm(self)

class DataValidator(base_validator.BaseValidator):
    def GetWindowData(self):
        win = self.GetWindow()
        if self.key == 'name':
            return win.GetValue()
        elif self.key == 'parent':
            index = win.GetSelection()
            if index>0:
                category_txt = win.GetStringSelection()
                session = pos.database.session()
                return session.query(Category).filter_by(display=category_txt).one()
            else:
                return None
    
    def ValidateWindowData(self, data):
        return True
    
    def SetWindowData(self, data):
        win = self.GetWindow()
        if self.key == 'name':
            win.SetValue(data)
        elif self.key == 'parent':
            if data is None:
                win.SetSelection(0)
            else:
                win.SetStringSelection(data.name)
