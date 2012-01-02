import wx

import pos

import pos.modules.user.objects.user as user
from pos.modules.user.objects.user import User
from pos.modules.user.objects.role import Role
from pos.modules.user.objects.permission import Permission

from pos.modules.base.panels import ManagePanel
from pos.modules.base.objects import validator as base_validator
from pos.modules.base.objects.formatter import TextFormatter

class UsersPanel(ManagePanel):
    def __init__(self, parent):
        ManagePanel.__init__(self, parent, -1, 'Users', User, DataValidator)

        self.createField('Username', wx.TextCtrl, 'username', '')
        self.createField('Role', wx.Choice, 'role', None)
        self.getField('role').Bind(wx.EVT_CHOICE, self.OnRoleChoice)
        self.createField('Permissions', wx.ListBox, 'permissions', [])
        self.createField('Login Box Appearance', wx.CheckBox, 'hidden', False,
                         label='Is Hidden')
        self.createField(None, wx.CheckBox, 'passwordCheck', False,
                         label='Change Password')
        self.getField('passwordCheck').Bind(wx.EVT_CHECKBOX, self.OnPasswordCheckbox)
        self.createField('Password', wx.TextCtrl, 'password1', '',
                         style=wx.TE_PASSWORD)
        self.createField('Confirm Password', wx.TextCtrl, 'password2', '',
                         style=wx.TE_PASSWORD)
        self._init_fields()

    canEditItem = lambda self, u: user.current != u
    canDeleteItem = lambda self, u: user.current != u

    def fillForm(self):
        item = self.getCurrentItem()
        if item is None: return
        data = {'username': item.username, 'role': item.role,
                 'permissions': item.role.permissions,
                 'password1': '', 'password2': '',
                 'passwordCheck': False}
        self.formPanel.fillForm(item=None, data=data)

    def newItem(self):
        data = self.formPanel.data
        if not data['passwordCheck']:
            data['password'] = ''
        return ManagePanel.newItem(self)
    
    def updateItem(self, item):
        data = self.formPanel.data
        if data['passwordCheck']:
            data['password'] = data['password1']
        try:
            del data['passwordCheck']
        except KeyError: pass
        try:
            del data['password2']
        except KeyError: pass
        try:
            del data['password1']
        except KeyError: pass
        try:
            del data['permissions']
        except KeyError: pass
        return ManagePanel.updateItem(self, item)

    def OnRoleChoice(self, event):
        event.Skip()
        role_txt = event.GetString()
        session = pos.database.session()
        r = session.query(Role).filter_by(display=role_txt).one()
        self.getField('permissions').Set([p.display for p in r.permissions])

    def OnPasswordCheckbox(self, event):
        event.Skip()
        enable_password = self.getField('passwordCheck').IsChecked()
        self.getField('password1').Enable(enable_password)
        self.getField('password2').Enable(enable_password)

class DataValidator(base_validator.BaseValidator):
    def GetWindowData(self):
        win = self.GetWindow()
        if self.key == 'username':
            return win.GetValue()
        elif self.key in ('password1', 'password2', 'passwordCheck'):
            return win.GetValue()
        elif self.key == 'role':
            role_txt = win.GetStringSelection()
            session = pos.database.session()
            return session.query(Role).filter_by(display=role_txt).one()
        elif self.key == 'permissions':
            return None
        elif self.key == 'hidden':
            return win.GetValue()
        elif self.key == 'passwordCheck':
            return win.GetValue()
    
    def ValidateWindowData(self, data):
        if self.key in ('password1', 'password2'):
            if self.panel.getField('passwordCheck').GetValue() and \
                    self.panel.getField('password1').GetValue() != self.panel.getField('password2').GetValue():
                wx.MessageBox('Passwords do not match', 'Error', wx.OK)
                return False
        return True
    
    def SetWindowData(self, data):
        win = self.GetWindow()
        if self.key == 'username':
            win.SetValue(data)
            if data != '':
                win.Enable(False)
            else:
                win.Enable(True)
        elif self.key == 'permissions':
            win.Set([p.display for p in data])
        elif self.key == 'role':
            session = pos.database.session()
            roles_txt = session.query(Role.display).all()
            win.SetItems([r[0] for r in roles_txt])
            if data is None:
                win.SetSelection(-1)
            else:
                win.SetStringSelection(data.display)
        elif self.key == 'passwordCheck':
            win.SetValue(data)
            self.panel.getField('password1').Enable(data)
            self.panel.getField('password2').Enable(data)
        elif self.key in ('password1', 'password2'):
            win.SetValue(data)
        elif self.key == 'hidden':
            win.SetValue(data)
