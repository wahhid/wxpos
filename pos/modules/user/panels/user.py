import wx

from pos.modules.base.objects.idManager import ids

import pos.modules.user.objects.user as user
import pos.modules.user.objects.role as role
import pos.modules.user.objects.permission as permission

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
        self.formPanel = wx.Panel(self, ids['userPanel.formPanel'])
        
        self.usernameLbl = wx.StaticText(self.formPanel, ids['userPanel.usernameLbl'],
                                      label='Username')
        self.usernameTxt = wx.TextCtrl(self.formPanel, ids['userPanel.usernameTxt'])
        
        self.roleLbl = wx.StaticText(self.formPanel, ids['userPanel.roleLbl'],
                                      label='Role')
        self.roleChoice = wx.Choice(self.formPanel, ids['userPanel.roleChoice'])
        
        self.permissionLbl = wx.StaticText(self.formPanel, ids['userPanel.permissionLbl'],
                                      label='Permissions')
        self.permissionList = wx.ListCtrl(self.formPanel, ids['userPanel.permissionList'],
                                            style=wx.LC_LIST)

        self.passwordCheck = wx.CheckBox(self.formPanel, ids['userPanel.passwordCheck'], label='Change Password')
        self.passwordCheck.Bind(wx.EVT_CHECKBOX, self.OnPasswordCheckbox, id=ids['userPanel.passwordCheck'])
        
        self.passwordSeperator = wx.StaticLine(self.formPanel, ids['userPanel.passwordSeperator'],)
        
        self.password1Lbl = wx.StaticText(self.formPanel, ids['userPanel.password1Lbl'],
                                      label='New Password')
        self.password1Txt = wx.TextCtrl(self.formPanel, ids['userPanel.password1Txt'],
                                        style=wx.TE_PASSWORD)
        
        self.password2Lbl = wx.StaticText(self.formPanel, ids['userPanel.password2Lbl'],
                                      label='Confirm Password')
        self.password2Txt = wx.TextCtrl(self.formPanel, ids['userPanel.password2Txt'],
                                        style=wx.TE_PASSWORD)
        
        self.saveBtn = wx.Button(self, ids['userPanel.saveBtn'], label='Save')
        self.saveBtn.Bind(wx.EVT_BUTTON, self.OnSaveButton,
              id=ids['userPanel.saveBtn'])

        self.resetBtn = wx.Button(self, ids['userPanel.resetBtn'], label='Reset')
        self.resetBtn.Bind(wx.EVT_BUTTON, self.OnResetButton,
              id=ids['userPanel.resetBtn'])
    
    def __init__(self, parent):
        wx.Panel.__init__(self, id=ids['userPanel'],
                parent=parent, style=wx.TAB_TRAVERSAL)

        self._init_main()
        self._init_sizers()

        self.updateRoleList()

        self.resetForm()

    def updateRoleList(self):
        self.roleChoice.SetItems(map(lambda r: r.data['name'], role.find(list=True)))

    def resetForm(self):
        u = user.current
        r = u.data['role']
        self.usernameTxt.SetValue(u.data['username'])
        self.roleChoice.SetStringSelection(r.data['name'])
        
        self.permissionList.ClearAll()
        for p in r.data['permissions']:
            item = wx.ListItem()
            item.SetText(p.data['name'])
            self.permissionList.InsertItem(item)

        self.password1Txt.SetValue('')
        self.password2Txt.SetValue('')

        self.usernameTxt.Enable(False)
        self.roleChoice.Enable(False)
        self.passwordCheck.SetValue(False)
        self.password1Txt.Enable(False)
        self.password2Txt.Enable(False)

    def updateUser(self):
        u = user.current
        password1, password2 = self.password1Txt.GetValue(), self.password2Txt.GetValue()
        if self.passwordCheck.IsChecked() and password1 != password2:
            wx.MessageBox('Passwords do not match', 'User Management',
                          wx.OK)
            return False
        elif self.passwordCheck.IsChecked() and password1 == '':
            retCode = wx.MessageBox('Set an empty password?', 'Empty password',
                                    wx.YES_NO | wx.ICON_QUESTION)
            if retCode != wx.YES:
                return False
        
        password = password1 if self.passwordCheck.IsChecked() else None
        return u.update(password=password)

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
