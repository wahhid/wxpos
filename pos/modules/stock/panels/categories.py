import wx

from pos.modules.base.objects.idManager import ids

import pos.modules.stock.objects.product as product
import pos.modules.stock.objects.category as category

from pos.modules.base.panels import ManagePanel

class CategoriesPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, ids['categoriesPanel'],
                style=wx.TAB_TRAVERSAL)
        
        self._init_panel('Categories', DataValidator)
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Parent Category', wx.Choice, 'parent_category', None)
        self._init_fields()

    getItems = lambda self: [{'text': c.data['name']} for c in category.find(list=True)]
    getItem = lambda self, item: category.find(name=item.GetText())
    newItem = lambda self: category.add(**self.data)
    updateItem = lambda self, c: c.update(**self.data)
    canEditItem = lambda self, c: True
    
    def canDeleteItem(self, c):
        if len(category.find(list=True, parent_category=c))>0:
            return False
        if len(product.find(list=True, category=c))>0:
            return False
        return True
    
    def fillData(self):
        category_choices = category.find(list=True)
        c = self.getCurrentItem()
        try:
            category_choices.remove(c)
        except ValueError:
            pass
        choices = ['[None]']+map(lambda c: c.data['name'], category_choices)
        self.getField('parent_category').SetItems(choices)
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
            if self.key == 'name':
                if len(data) == 0:
                    return False
            elif self.key == 'parent_category':
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
            elif self.key == 'parent_category':
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
        elif self.key == 'parent_category':
            index = win.GetSelection()
            if index>0:
                category_name = win.GetStringSelection()
                data = category.find(name=category_name)
            else:
                data = None
        return data
                
