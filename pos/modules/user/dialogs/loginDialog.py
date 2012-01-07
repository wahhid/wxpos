import wx

import pos

from sqlalchemy.orm import exc

import pos.modules.user.objects.user as user
from pos.modules.user.objects.superuser import SuperUser
from pos.modules.user.objects.user import User

from pos.modules.user.windows import UserCatalogList

class LoginDialog(wx.Dialog):
    def __init_ctrls(self):
        self.panel = wx.Panel(self, -1)

        # User
        self.userLbl = wx.StaticText(self.panel, -1, label='User')
        self.userList = UserCatalogList(self.panel)
        self.userList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnUserListActivate)
        
        # Password
        self.passwordLbl = wx.StaticText(self.panel, -1, label='Password')
        self.passwordTxt = wx.TextCtrl(self.panel, -1, style=wx.TE_PASSWORD)

        # Controls
        self.loginBtn = wx.Button(self, wx.ID_OK, label='Login')
        self.exitBtn = wx.Button(self, wx.ID_CANCEL, label='Exit')
    
    def __init_sizers(self):
        self.passwordSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.passwordSizer.Add(self.passwordLbl, 0, border=10, flag=wx.RIGHT | wx.ALIGN_LEFT)
        self.passwordSizer.Add(self.passwordTxt, 1, border=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT)
        
        self.panelSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.panelSizer.Add(self.userLbl, 0, flag=wx.ALL | wx.ALIGN_LEFT)
        self.panelSizer.Add(wx.Size(0, 0), 0, border=5, flag=wx.ALL)
        self.panelSizer.Add(self.userList, 1, flag=wx.EXPAND | wx.ALL)
        self.panelSizer.Add(wx.Size(0, 0), 0, border=5, flag=wx.ALL)
        self.panelSizer.AddSizer(self.passwordSizer, 0, flag=wx.EXPAND | wx.ALL)
        self.panelSizer.Fit(self.panel)
        self.panel.SetSizer(self.panelSizer)

        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL)
        self.controlSizer.Add(self.loginBtn, 0, flag=wx.CENTER | wx.ALL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL)
        self.controlSizer.Add(self.exitBtn, 0, flag=wx.CENTER | wx.ALL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL) 
        
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.Add(self.panel, 1, border=10, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.AddSizer(self.controlSizer, 0, border=10, flag=wx.BOTTOM | wx.LEFT | wx.RIGHT | wx.EXPAND)
        self.SetSizer(self.mainSizer)
    
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, size=wx.Size(400, 500), title='Login')

        F3CommandId = wx.NewId()
        accTable = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_F3, F3CommandId)])
        self.Bind(wx.EVT_MENU, self.OnF3Command, id=F3CommandId) 
        self.SetAcceleratorTable(accTable)

        self.__init_ctrls()
        self.__init_sizers()

        self.panel.SetValidator(LoginValidator())
    
    def OnUserListActivate(self, event):
        event.Skip()
        self.passwordTxt.SetFocus()
        self.passwordTxt.SelectAll()
    
    def OnF3Command(self, event):
        event.Skip()
        dlg = HiddenUserLoginDialog(None)
        dlg.ShowModal()
        if dlg.success:
            user.current = dlg.user
            self.Close()

class HiddenUserLoginDialog(wx.Dialog):
    def __init_ctrls(self):
        self.panel = wx.Panel(self, -1)

        # User
        self.usernameLbl = wx.StaticText(self.panel, -1, label='Username')
        self.usernameTxt = wx.TextCtrl(self.panel, -1)
        
        # Password
        self.passwordLbl = wx.StaticText(self.panel, -1, label='Password')
        self.passwordTxt = wx.TextCtrl(self.panel, -1, style=wx.TE_PASSWORD)

        # Controls
        self.okBtn = wx.Button(self, wx.ID_OK, label='OK')
        self.okBtn.Bind(wx.EVT_BUTTON, self.OnOkButton)
        self.cancelBtn = wx.Button(self, wx.ID_CANCEL, label='Cancel')
    
    def __init_sizers(self):
        self.panelSizer = wx.GridSizer(hgap=5, vgap=5, cols=2)
        self.panelSizer.Add(self.usernameLbl, 0, flag=wx.ALL | wx.ALIGN_LEFT)
        self.panelSizer.Add(self.usernameTxt, 1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT)
        self.panelSizer.Add(self.passwordLbl, 0, flag=wx.ALL | wx.ALIGN_LEFT)
        self.panelSizer.Add(self.passwordTxt, 1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT)
        self.panel.SetSizerAndFit(self.panelSizer)

        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL)
        self.controlSizer.Add(self.okBtn, 0, flag=wx.CENTER | wx.ALL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL)
        self.controlSizer.Add(self.cancelBtn, 0, flag=wx.CENTER | wx.ALL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL) 
        
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.Add(self.panel, 1, border=10, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.AddSizer(self.controlSizer, 0, border=10, flag=wx.BOTTOM | wx.LEFT | wx.RIGHT | wx.EXPAND)
        self.SetSizerAndFit(self.mainSizer)
    
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, title='Login')

        self.__init_ctrls()
        self.__init_sizers()
        
        self.success = False
        self.user = None
    
    def OnOkButton(self, event):
        username = self.usernameTxt.GetValue()
        password = self.passwordTxt.GetValue()
        if username == '_superuser_':
            self.user = SuperUser()
        else:
            session = pos.database.session()
            try:
                self.user = session.query(User).filter(User.username == username).one()
            except exc.NoResultFound, exc.MultipleResultsFound:
                pass
        if self.user is not None and self.user.login(password):
            self.success = True
            event.Skip()
        else:
            wx.MessageBox('Invalid username/password.', 'Error', style=wx.OK | wx.ICON_EXCLAMATION)
            self.usernameTxt.SetFocus()
            self.usernameTxt.SelectAll()

class LoginValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.user = None

    Clone = lambda self: LoginValidator()

    def Validate(self, parent):
        password = parent.passwordTxt.GetValue()
        u = parent.userList.GetValue()
        
        password_valid = True
        username_valid = u is not None
        
        if not username_valid:
            wx.MessageBox(message='Select a user', caption='Failure',
                                style=wx.OK, parent=None)
            return False
        elif not password_valid:
            wx.MessageBox(message='Invalid password', caption='Failure',
                                style=wx.OK, parent=None)
            return False
        else:
            if not u.login(password):
                wx.MessageBox(message='Wrong username/password', caption='Failure',
                                    style=wx.OK, parent=None)
                return False
            else:
                self.user = u
                return True

    def TransferToWindow(self):
        user.current = None
        return True

    def TransferFromWindow(self):
        user.current = self.user
        return True
