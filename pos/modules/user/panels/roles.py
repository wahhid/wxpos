import wx

import pos

import pos.modules.user.objects.user as user
import pos.modules.user.objects.role as role
from pos.modules.user.objects.role import Role
from pos.modules.user.objects.permission import Permission

from pos.modules.base.panels import ManagePanel

class RolesPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)

        self._init_panel('Roles', DataValidator)
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Permissions', wx.CheckListBox, 'permissions', [])
        self._init_fields()

    getItems = lambda self: pos.database.session().query(Role, Role.name).all()
    newItem = lambda self: role.add(**self.data)
    updateItem = lambda self, r: r.update(**self.data)
    canEditItem = lambda self, r: user.current.role != r
    canDeleteItem = lambda self, r: len(r.users) == 0
    
    def fillData(self):
        session = pos.database.session()
        permission_names = session.query(Permission.name).all()
        self.getField('permissions').Set([p[0] for p in permission_names])
        r = self.getCurrentItem()
        if r is None: return
        self.getField('name').Enable(False)
        r.fillDict(self.data)

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
            elif self.key == 'permissions':
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
            elif self.key == 'permissions':
                checked_indices = [win.FindString(p.name) for p in data]
                for i in range(win.GetCount()):
                    win.Check(i, i in checked_indices)
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
        elif self.key == 'permissions':
            session = pos.database.session()
            data = session.query(Permission).filter(Permission.name.in_(win.CheckedStrings)).all()
        return data
