import wx

from pos.modules.base.objects.idManager import ids

import pos.modules.user.objects.user as user
import pos.modules.user.objects.role as role
import pos.modules.user.objects.permission as permission

from pos.modules.base.panels import ManagePanel

class UsersPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, ids['usersPanel'],
                style=wx.TAB_TRAVERSAL)

        self._init_panel('Users', DataValidator)
        self.createField('Username', wx.TextCtrl, 'username', '')
        self.createField('Role', wx.Choice, 'role', None)
        self.createField('Permissions', wx.ListCtrl, 'permissions', [],
                         style=wx.LC_LIST)
        self.createField(None, wx.CheckBox, 'passwordCheck', False,
                         label='Change Password')
        self.createField('Password', wx.TextCtrl, 'password1', '',
                         style=wx.TE_PASSWORD)
        self.createField('Confirm Password', wx.TextCtrl, 'password2', '',
                         style=wx.TE_PASSWORD)
        self._init_fields()

        self.getField('passwordCheck').Bind(wx.EVT_CHECKBOX, self.OnPasswordCheckbox)
        self.getField('role').Bind(wx.EVT_CHOICE, self.OnRoleChoice)

    getItems = lambda self: [[u, u.data['username']] for u in user.find(list=True)]
    newItem = lambda self: user.add(username=self.data['username'], password=self.data['password1'], role=self.data['role'])
    def updateItem(self, u):
        if self.data['passwordCheck']:
            return u.update(password=self.data['password1'], role=self.data['role'])
        else:
            return u.update(role=self.data['role'])
    canEditItem = lambda self, u: user.current != u
    canDeleteItem = lambda self, u: user.current != u

    def fillData(self):
        self.getField('role').SetItems(map(lambda r: r.data['name'], role.find(list=True)))
        u = self.getCurrentItem()
        if u is None: return
        self.getField('username').Enable(False)
        self.data = {'username': u.data['username'], 'role': u.data['role'],
                     'permissions': u.data['role'].data['permissions'],
                     'password1': '', 'password2': '',
                     'passwordCheck': False}

    def OnRoleChoice(self, event):
        event.Skip()
        role_name = event.GetString()
        self.getField('permissions').ClearAll()
        for p in role.find(name=role_name).data['permissions']:
            item = wx.ListItem()
            item.SetText(p.data['name'])
            self.getField('permissions').InsertItem(item)

    def OnPasswordCheckbox(self, event):
        event.Skip()
        enable_password = self.getField('passwordCheck').IsChecked()
        self.getField('password1').Enable(enable_password)
        self.getField('password2').Enable(enable_password)

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
            if self.key == 'username':
                return True
            elif self.key == 'role':
                return True
            elif self.key == 'permissions':
                return True
            elif self.key == 'passwordCheck':
                return True
            elif self.key in ('password1', 'password2'):
                if self.panel.getField('passwordCheck').IsChecked() and \
                       self.panel.getField('password1').GetValue() != self.panel.getField('password2').GetValue():
                    wx.MessageBox('Passwords do not match', 'Edit User',
                                  wx.OK)
                    return False
        except:
            print '-- ERROR -- in DataValidator.TransferToWindow'
            print '--', self.key, self.panel.data
            raise
        return True

    def TransferToWindow(self):
        try:
            win = self.GetWindow()
            data = self.panel.data[self.key]
            if self.key == 'username':
                win.SetValue(data)
            elif self.key == 'role':
                if data is None:
                    win.SetSelection(-1)
                else:
                    win.SetStringSelection(data.data['name'])
            elif self.key == 'permissions':
                win.ClearAll()
                for p in data:
                    item = wx.ListItem()
                    item.SetText(p.data['name'])
                    win.InsertItem(item)
            elif self.key == 'passwordCheck':
                win.SetValue(data)
                enable_password = win.IsChecked()
                self.panel.getField('password1').Enable(enable_password)
                self.panel.getField('password2').Enable(enable_password)
            elif self.key in ('password1', 'password2'):
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
        if self.key == 'username':
            data = win.GetValue()
        elif self.key == 'role':
            data = role.find(name=win.GetStringSelection())
        elif self.key == 'permissions':
            data = None
        elif self.key == 'passwordCheck':
            data = win.GetValue()
        elif self.key in ('password1', 'password2'):
            data = win.GetValue()
        return data
