import wx

import pos

import pos.modules.user.objects.permission as permission
from pos.modules.user.objects.permission import Permission
from pos.modules.user.objects.role import Role

from pos.modules.base.panels import ManagePanel

class PermissionsPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)
        
        self._init_panel('Permissions', DataValidator)
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Description', wx.TextCtrl, 'description', '',
                         style=wx.TE_MULTILINE)
        self._init_fields()

    getItems = lambda self: pos.database.session().query(Permission, Permission.name).all()
    newItem = lambda self: permission.add(**self.data)
    updateItem = lambda self, p: p.update(**self.data)
    canEditItem = lambda self, p: True
    canDeleteItem = lambda self, p: len(p.roles) == 0
    
    def fillData(self):
        p = self.getCurrentItem()
        if p is None: return
        self.getField('name').Enable(False)
        p.fillDict(self.data)

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
            elif self.key == 'description':
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
            if self.key in ('name', 'description'):
                win.SetValue(data)
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
        if self.key in ('name', 'description'):
            data = win.GetValue()
        return data
                
