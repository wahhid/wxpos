import wx

import pos

import pos.modules.customer.objects.customergroup as customergroup
from pos.modules.customer.objects.customergroup import CustomerGroup

from pos.modules.base.panels import ManagePanel

class CustomerGroupsPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)
        
        self._init_panel('Customer Groups', DataValidator)
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Comment', wx.TextCtrl, 'comment', None,
                         style=wx.TE_MULTILINE)
        self._init_fields()

    getItems = lambda self: pos.database.session().query(CustomerGroup, CustomerGroup.name).all()
    newItem = lambda self: customergroup.add(**self.data)
    updateItem = lambda self, cg: cg.update(**self.data)
    canEditItem = lambda self, cg: True
    canDeleteItem = lambda self, cg: True
    
    def fillData(self):
        cg = self.getCurrentItem()
        if cg is None: return
        cg.fillDict(self.data)

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
            if self.key == 'name':
                win.SetValue(data)
            elif self.key == 'comment':
                if data is None:
                   win.SetValue('')
                else:
                    win.SetValue(data)
        except:
            print '-- ERROR -- in DataValidator.TransferToWindow'
            print '--', self.key, self.panel.data
            raise
        return True

    def TransferFromWindow(self):
        try:
            win = self.GetWindow()
            if self.key == 'name':
                data = win.GetValue()
            elif self.key == 'comment':
                data = win.GetValue()
                if data == '':
                    data = None
            self.panel.data[self.key] = data
        except:
            print '-- ERROR -- in DataValidator.TransferFromWindow'
            print '--', self.key, self.panel.data
            raise
        return True