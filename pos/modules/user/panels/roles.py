import wx

from pos.modules.base.objects.idManager import ids

import pos.modules.user.objects.user as user
import pos.modules.user.objects.role as role
import pos.modules.user.objects.permission as permission

from pos.modules.base.panels import ManagePanel

class RolesPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, ids['rolesPanel'],
                style=wx.TAB_TRAVERSAL)

        self._init_panel('Roles', DataValidator)
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Permissions', wx.CheckListBox, 'permissions', [])
        self._init_fields()

    getItems = lambda self: [{'text': r.data['name']} for r in role.find(list=True)]
    getItem = lambda self, item: role.find(name=item.GetText())
    newItem = lambda self: role.add(**self.data)
    updateItem = lambda self, r: r.update(**self.data)
    canEditItem = lambda self, r: user.current.data['role'] != r
    canDeleteItem = lambda self, r: user.find(role=r) is None
    
    def fillData(self):
        self.getField('permissions').Set(map(lambda p: p.data['name'], permission.find(list=True)))
        r = self.getCurrentItem()
        if r is None: return
        self.getField('name').Enable(False)
        self.data = r.data.copy()

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
                checked_indices = []
                for p in data:
                    index = win.FindString(p.data['name'])
                    checked_indices.append(index)
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
            data = map(lambda pname: permission.find(name=pname), win.CheckedStrings)
        return data
