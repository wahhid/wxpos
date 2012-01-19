import wx

import pos

import pos.modules.user.objects.user as user

from pos.modules.base.panels import FormPanel
from pos.modules.base.objects import validator as base_validator
from pos.modules.base.objects.formatter import TextFormatter

class IndividualUserPanel(wx.PyPanel):
    def _init_sizers(self):
        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        controls = [self.saveBtn, self.cancelBtn]
        for c in controls:
            self.controlSizer.Add(c, 0, border=10, flag=wx.RIGHT)
        
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.Add(self.controlSizer, 0, flag=wx.EXPAND | wx.RIGHT | wx.LEFT)
        self.mainSizer.Add(self.formPanel, 1, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(self.mainSizer)

    def _init_main(self):
        self.saveBtn = wx.Button(self, -1, label='Save')
        self.saveBtn.Bind(wx.EVT_BUTTON, self.OnSaveButton)

        self.cancelBtn = wx.Button(self, -1, label='Cancel')
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancelButton)
        
        self.formPanel = UserFormPanel(self)
    
    def __init__(self, parent):
        wx.PyPanel.__init__(self, parent, -1)
        
        self._init_main()
        self._init_sizers()
        
        self.formPanel.getField('passwordCheck').Bind(wx.EVT_CHECKBOX, self.OnPasswordCheckbox)
        
        self.resetForm()
        
    def resetForm(self):
        data = {'username': user.current.username, 'role': user.current.role}
        self.formPanel.fillForm(data=data)
        self.resetControls()
    
    def resetControls(self):
        enable_password = self.formPanel.getField('passwordCheck').IsChecked()
        self.formPanel.getField('password1').Enable(enable_password)
        self.formPanel.getField('password2').Enable(enable_password)
        self.saveBtn.Enable(enable_password)
        self.cancelBtn.Enable(enable_password)
    
    def updateUser(self):
        if self.formPanel.data['passwordCheck']:
            user.current.update(password=self.formPanel.data['password1'])
        return True

    def validatePasswords(self):
        if self.formPanel.data['password1'] != self.formPanel.data['password2']:
            wx.MessageBox('Passwords do not match', 'Error', wx.OK)
            return False
        elif self.formPanel.data['password1'] == '':
            allow = pos.config['mod.user', 'allow_empty_passwords']
            if bool(allow):
                retCode = wx.MessageBox('Set an empty password?', 'Empty password?',
                                        wx.YES_NO | wx.ICON_QUESTION)
                return retCode == wx.YES
            else:
                wx.MessageBox('Empty passwords are not allowed.', 'Error', wx.OK)
                return False
        else:
            return True

    def OnSaveButton(self, event):
        if not self.formPanel.Validate():
            wx.MessageBox('The form contains some invalid fields.\nCannot save changes.', 'Error', wx.OK)
            return
        self.formPanel.TransferDataFromWindow()
        if not self.validatePasswords():
            return
        if self.updateUser():
            self.resetForm()
        event.Skip()

    def OnCancelButton(self, event):
        self.resetForm()
        event.Skip()

    def OnPasswordCheckbox(self, event):
        event.Skip()
        self.resetControls()

class UserFormPanel(FormPanel):
    def __init__(self, parent):
        FormPanel.__init__(self, parent, -1, DataValidator)
        
        self.createField('Username', wx.TextCtrl, 'username', '')
        self.createField('Role', wx.TextCtrl, 'role', None)
        self.createField(None, wx.CheckBox, 'passwordCheck', False,
                         label='Change Password')
        self.createField('Password', wx.TextCtrl, 'password1', '',
                         style=wx.TE_PASSWORD)
        self.createField('Confirm Password', wx.TextCtrl, 'password2', '',
                         style=wx.TE_PASSWORD)
        self._init_fields()

class DataValidator(base_validator.BaseValidator):
    def GetWindowData(self):
        win = self.GetWindow()
        if self.key in ('password1', 'password2', 'passwordCheck'):
            return win.GetValue()
        elif self.key == 'username':
            return win.GetValue()
        elif self.key == 'role':
            return None
    
    def SetWindowData(self, data):
        win = self.GetWindow()
        if self.key == 'username':
            win.Enable(False)
            win.SetValue(data)
        elif self.key == 'role':
            win.Enable(False)
            if data is None:
                win.SetValue('')
            else:
                win.SetValue(data.display)
        elif self.key in ('password1', 'password2'):
            win.SetValue('')
        elif self.key == 'passwordCheck':
            self.panel.getField('password1').Enable(data)
            self.panel.getField('password2').Enable(data)
            win.SetValue(data)
