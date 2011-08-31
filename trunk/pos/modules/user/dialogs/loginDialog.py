import wx

from pos.modules.base.objects.idManager import ids

import pos.modules.user.objects.user as user

class LoginDialog(wx.Dialog):
    def __init_ctrls(self):
        self.panel = wx.Panel(self, ids['loginPanel'])

        # User
        self.userLbl = wx.StaticText(self.panel, -1, label='User')
        self.userList = wx.ListCtrl(self.panel, -1, style=wx.LC_ICON)
        
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
        wx.Dialog.__init__(self, parent, ids['loginDialog'],
              size=wx.Size(400, 500), title='Login')

        self.__init_ctrls()
        self.__init_sizers()

        self.panel.SetValidator(LoginValidator())
        
        users = user.find(list=True)
        il = wx.ImageList(32, 32, True)
        il.Add(wx.Bitmap('images/user.png', wx.BITMAP_TYPE_PNG))
        self.userList.AssignImageList(il, 0)
        for index, u in enumerate(users):
            self.userList.InsertImageStringItem(index, u.data['username'], 0)

class LoginValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.user = None

    Clone = lambda self: LoginValidator()

    def Validate(self, parent):
        password = parent.passwordTxt.GetValue()
        selected_user = parent.userList.GetFirstSelected()
        
        password_valid = True
        username_valid = selected_user >= 0
        
        if not username_valid:
            wx.MessageBox(message='Select a user', caption='Failure',
                                style=wx.OK, parent=None)
            return False
        elif not password_valid:
            wx.MessageBox(message='Invalid password', caption='Failure',
                                style=wx.OK, parent=None)
            return False
        else:
            username = parent.userList.GetItemText(selected_user)
            u = user.find(username=username)
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
