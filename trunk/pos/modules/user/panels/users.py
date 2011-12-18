import wx

import pos

import pos.modules.user.objects.user as user
from pos.modules.user.objects.user import User
from pos.modules.user.objects.role import Role
from pos.modules.user.objects.permission import Permission

from pos.modules.base.panels import ManagePanel

class UsersPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)

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

    getItems = lambda self: pos.database.session().query(User, User.username).all()
    newItem = lambda self: user.add(username=self.data['username'], password=self.data['password1'], role=self.data['role'])
    def updateItem(self, u):
        if self.data['passwordCheck']:
            return u.update(password=self.data['password1'], role=self.data['role'])
        else:
            return u.update(role=self.data['role'])
    canEditItem = lambda self, u: user.current != u
    canDeleteItem = lambda self, u: user.current != u

    def fillData(self):
        session = pos.database.session()
        role_names = session.query(Role.name).all()
        self.getField('role').SetItems([r[0] for r in role_names])
        u = self.getCurrentItem()
        if u is None: return
        self.getField('username').Enable(False)
        self.data = {'username': u.username, 'role': u.role,
                     'permissions': u.role.permissions,
                     'password1': '', 'password2': '',
                     'passwordCheck': False}

    def OnRoleChoice(self, event):
        event.Skip()
        role_name = event.GetString()
        session = pos.database.session()
        r = session.query(Role).filter_by(name=role_name).one()
        self.getField('permissions').ClearAll()
        for p in r.permissions:
            item = wx.ListItem()
            item.SetText(p.name)
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
                    win.SetStringSelection(data.name)
            elif self.key == 'permissions':
                win.ClearAll()
                for p in data:
                    item = wx.ListItem()
                    item.SetText(p.name)
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
            session = pos.database.session()
            data = session.query(Role).filter_by(name=win.GetStringSelection()).one()
        elif self.key == 'permissions':
            data = None
        elif self.key == 'passwordCheck':
            data = win.GetValue()
        elif self.key in ('password1', 'password2'):
            data = win.GetValue()
        return data
