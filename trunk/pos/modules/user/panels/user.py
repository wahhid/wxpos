import wx

import pos

import pos.modules.user.objects.user as user

from pos.modules.base.panels import FormPanel
from pos.modules.base.objects import validator as base_validator
from pos.modules.base.objects.formatter import TextFormatter

class IndividualUserPanel(FormPanel):
    """
    def _init_sizers(self):
        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        controls = [self.saveBtn, self.resetBtn]
        for c in controls:
            self.controlSizer.Add(c, 0, border=10, flag=wx.RIGHT)

    def _init_main(self):
        self.saveBtn = wx.Button(self, -1, label='Save')
        self.saveBtn.Bind(wx.EVT_BUTTON, self.OnSaveButton)

        self.resetBtn = wx.Button(self, -1, label='Reset')
        self.resetBtn.Bind(wx.EVT_BUTTON, self.OnResetButton)
    """
    
    def __init__(self, parent):
        FormPanel.__init__(self, parent, -1, DataValidator)
        
        self.createField('Username', wx.TextCtrl, 'username', '', formatter=TextFormatter(required=True))
        self.createField('Role', wx.TextCtrl, 'role', None)
        self.createField(None, wx.CheckBox, 'passwordCheck', False,
                         label='Change Password')
        self.getField('passwordCheck').Bind(wx.EVT_CHECKBOX, self.OnPasswordCheckbox)
        self.createField('Password', wx.TextCtrl, 'password1', '',
                         style=wx.TE_PASSWORD)
        self.createField('Confirm Password', wx.TextCtrl, 'password2', '',
                         style=wx.TE_PASSWORD)
        self._init_fields()
        
        data = {'username': user.current.username, 'role': user.current.role}
        self.fillForm(data=data)
    
    """
    def resetForm(self):
        user.current.fillDict(self.__data)
        FormPanel.resetForm(self)
    """
    
    def updateUser(self):
        user.current.update(password=self.data['password1'])

    def OnPasswordCheckbox(self, event):
        enable_password = self.getField('passwordCheck').IsChecked()
        self.getField('password1').Enable(enable_password)
        self.getField('password2').Enable(enable_password)
        event.Skip()

    def OnSaveButton(self, event):
        if not self.Validate():
            wx.MessageBox('The form contains some invalid fields.\nCannot save changes.', 'Error', wx.OK)
            return
        self.formPanel.TransferDataFromWindow()
        if self.updateUser():
            self.resetForm()
        event.Skip()

    def OnResetButton(self, event):
        self.resetForm()
        event.Skip()

class DataValidator(base_validator.BaseValidator):
    def GetWindowData(self):
        win = self.GetWindow()
        if self.key in ('password1', 'password2', 'passwordCheck'):
            return win.GetValue()
    
    def ValidateWindowData(self, data):
        if self.key in ('password1', 'password2') and self.data['passwordCheck']:
            if self.data['password1'] != data['password2']:
                wx.MessageBox('Passwords do not match', 'Error',
                              wx.OK)
                return False
            elif self.data['password1'] == '':
                allow = pos.config['mod.user', 'allow_empty_passwords']
                if bool(allow):
                    retCode = wx.MessageBox('Set an empty password?', 'Empty password?',
                                            wx.YES_NO | wx.ICON_QUESTION)
                    if retCode != wx.YES:
                        return False
                else:
                    wx.MessageBox('Empty passwords are not allowed.', 'Error',
                              wx.OK)
                    return False
        return True
    
    def SetWindowData(self, data):
        win = self.GetWindow()
        if self.key == 'username':
            win.Enable(False)
            win.SetValue(data)
        elif self.key == 'role':
            win.Enable(False)
            if data is not None:
                win.SetValue(data.display)
        elif self.key in ('password1', 'password2'):
            win.SetValue('')
        elif self.key == 'passwordCheck':
            win.SetValue(data)
