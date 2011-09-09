import wx

from pos.modules.base.objects.idManager import ids

import pos.modules.user.objects.user as user
import pos.modules.user.objects.role as role
import pos.modules.user.objects.permission as permission

from pos.modules.base.panels import ManagePanel

class PermissionsPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, ids['permissionsPanel'],
                style=wx.TAB_TRAVERSAL)
        
        self._init_panel('Permissions', DataValidator)
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Description', wx.TextCtrl, 'description', '',
                         style=wx.TE_MULTILINE)
        self._init_fields()

    getItems = lambda self: [[p, p.data['name']] for p in permission.find(list=True)]
    newItem = lambda self: permission.add(**self.data)
    updateItem = lambda self, p: p.update(**self.data)
    canEditItem = lambda self, p: True
    def canDeleteItem(self, p):
        roles = role.find(list=True)
        roles = filter(lambda r: r.isPermitted(p), roles)
        return len(roles) == 0
    
    def fillData(self):
        p = self.getCurrentItem()
        if p is None: return
        self.getField('name').Enable(False)
        self.data = p.data.copy()

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
                
