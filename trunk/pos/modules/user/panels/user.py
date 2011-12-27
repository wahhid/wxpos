import wx

import pos

import pos.modules.user.objects.user as user
from pos.modules.user.objects.role import Role

VIEW_MODE, EDIT_MODE = 0, 1

class IndividualUserPanel(wx.Panel):

    def _init_sizers(self):
        self.formSizer = wx.GridBagSizer(hgap=5, vgap=5)
        
        self.formSizer.Add(self.usernameLbl, (0, 0), flag=wx.EXPAND | wx.ALL)
        self.formSizer.Add(self.usernameTxt, (0, 1))
        
        self.formSizer.Add(self.roleLbl, (1, 0), flag=wx.EXPAND | wx.ALL)
        self.formSizer.Add(self.roleChoice, (1, 1))
        
        self.formSizer.Add(self.permissionLbl, (2, 0), flag=wx.EXPAND | wx.ALL)
        self.formSizer.Add(self.permissionList, (2, 1), flag=wx.EXPAND | wx.ALL)

        self.formSizer.Add(self.passwordCheck, (3, 0))
        self.formSizer.Add(self.passwordSeperator, (3, 1),
                           border=10, flag=wx.EXPAND | wx.ALL)

        self.formSizer.Add(self.password1Lbl, (4, 0), flag=wx.EXPAND | wx.ALL)
        self.formSizer.Add(self.password1Txt, (4, 1))
        
        self.formSizer.Add(self.password2Lbl, (5, 0), flag=wx.EXPAND | wx.ALL)
        self.formSizer.Add(self.password2Txt, (5, 1))

        self.formSizer.AddGrowableCol(1, 1)
        
        self.formPanel.SetSizer(self.formSizer)

        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        controls = [self.saveBtn, self.resetBtn]
        for c in controls:
            self.controlSizer.Add(c, 0, border=10, flag=wx.RIGHT)

        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.AddSizer(self.controlSizer, 0)
        self.mainSizer.Add(self.formPanel, 1, border=10, flag=wx.EXPAND | wx.ALL)

        self.SetSizer(self.mainSizer)

    def _init_main(self):
        self.formPanel = wx.Panel(self, -1)
        
        self.usernameLbl = wx.StaticText(self.formPanel, -1, label='Username')
        self.usernameTxt = wx.TextCtrl(self.formPanel, -1)
        
        self.roleLbl = wx.StaticText(self.formPanel, -1, label='Role')
        self.roleChoice = wx.Choice(self.formPanel, -1)
        
        self.permissionLbl = wx.StaticText(self.formPanel, -1, label='Permissions')
        self.permissionList = wx.ListCtrl(self.formPanel, -1, style=wx.LC_LIST)

        self.passwordCheck = wx.CheckBox(self.formPanel, -1, label='Change Password')
        self.passwordCheck.Bind(wx.EVT_CHECKBOX, self.OnPasswordCheckbox)
        
        self.passwordSeperator = wx.StaticLine(self.formPanel, -1)
        
        self.password1Lbl = wx.StaticText(self.formPanel, -1, label='New Password')
        self.password1Txt = wx.TextCtrl(self.formPanel, -1, style=wx.TE_PASSWORD)
        
        self.password2Lbl = wx.StaticText(self.formPanel, -1, label='Confirm Password')
        self.password2Txt = wx.TextCtrl(self.formPanel, -1, style=wx.TE_PASSWORD)
        
        self.saveBtn = wx.Button(self, -1, label='Save')
        self.saveBtn.Bind(wx.EVT_BUTTON, self.OnSaveButton)

        self.resetBtn = wx.Button(self, -1, label='Reset')
        self.resetBtn.Bind(wx.EVT_BUTTON, self.OnResetButton)
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)

        self._init_main()
        self._init_sizers()

        self.updateRoleList()

        self.resetForm()

    def updateRoleList(self):
        session = pos.database.session()
        role_names = session.query(Role.name).all()
        self.roleChoice.SetItems([r[0] for r in role_names])

    def resetForm(self):
        u = user.current
        r = u.role
        self.usernameTxt.SetValue(u.username)
        self.roleChoice.SetStringSelection(r.name)
        
        self.permissionList.ClearAll()
        for p in r.permissions:
            item = wx.ListItem()
            item.SetText(p.name)
            self.permissionList.InsertItem(item)

        self.password1Txt.SetValue('')
        self.password2Txt.SetValue('')

        self.usernameTxt.Enable(False)
        self.roleChoice.Enable(False)
        self.passwordCheck.SetValue(False)
        self.password1Txt.Enable(False)
        self.password2Txt.Enable(False)

    def updateUser(self):
        if self.passwordCheck.IsChecked():
            u = user.current
            password1, password2 = self.password1Txt.GetValue(), self.password2Txt.GetValue()
            if password1 != password2:
                wx.MessageBox('Passwords do not match', 'User Management',
                              wx.OK)
                return False
            elif password1 == '':
                allow = pos.config['mod.user', 'allow_empty_passwords']
                if bool(allow):
                    retCode = wx.MessageBox('Set an empty password?', 'Empty password',
                                            wx.YES_NO | wx.ICON_QUESTION)
                    if retCode != wx.YES:
                        return False
                else:
                    wx.MessageBox('Empty passwords are not allowed.', 'Empty password',
                              wx.OK)
                    return False
            return u.update(password=password1)
        else:
            return True

    def OnPasswordCheckbox(self, event):
        enable_password = self.passwordCheck.IsChecked()
        self.password1Txt.Enable(enable_password)
        self.password2Txt.Enable(enable_password)
        event.Skip()

    def OnSaveButton(self, event):
        if self.updateUser():
            self.resetForm()
        event.Skip()

    def OnResetButton(self, event):
        self.resetForm()
        event.Skip()
