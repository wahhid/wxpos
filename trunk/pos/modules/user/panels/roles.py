import wx

import pos

import pos.modules.user.objects.user as user
from pos.modules.user.objects.role import Role
from pos.modules.user.objects.permission import Permission

from pos.modules.base.panels import ManagePanel
from pos.modules.base.objects import validator as base_validator

class RolesPanel(ManagePanel):
    def __init__(self, parent):
        ManagePanel.__init__(self, parent, -1, 'Roles', Role, DataValidator)

        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Permissions', wx.CheckListBox, 'permissions', [])
        self._init_fields()

    canEditItem = lambda self, r: user.current.role != r
    canDeleteItem = lambda self, r: len(r.users) == 0

class DataValidator(base_validator.BaseValidator):
    def GetWindowData(self):
        win = self.GetWindow()
        if self.key == 'name':
            return win.GetValue()
        elif self.key == 'permissions':
            session = pos.database.session()
            return session.query(Permission).filter(Permission.name.in_(win.CheckedStrings)).all()
    
    def ValidateWindowData(self, data):
        if self.key == 'name':
            return data != ''
        elif self.key == 'permissions':
            return len(data)>0
        return True
    
    def SetWindowData(self, data):
        win = self.GetWindow()
        if self.key == 'name':
            win.SetValue(data)
            if data != '':
                win.Enable(False)
            else:
                win.Enable(True)
        elif self.key == 'permissions':
            session = pos.database.session()
            permissions_txt = session.query(Permission.display).all()
            win.Set([p[0] for p in permissions_txt])
            
            checked_indices = [win.FindString(p.display) for p in data]
            for i in range(win.GetCount()):
                win.Check(i, i in checked_indices)
