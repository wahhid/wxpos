import wx

import ConfigParser

import pos

config = ConfigParser.SafeConfigParser()
config.read('wxpos.cfg')

if not config.has_section('MySQL'):
    config.add_section('MySQL')

class ConfigDialog(wx.Dialog):
    def __init_ctrls(self):
        self.dbPanel = DatabaseConfigPanel(self)
        
        self.okBtn = wx.Button(self, wx.ID_OK, label='OK')
        self.okBtn.Bind(wx.EVT_BUTTON, self.OnOkButton)

        self.cancelBtn = wx.Button(self, wx.ID_CANCEL, label='Cancel')
    
    def __init_sizers(self):
        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlSizer.Add(self.okBtn, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.controlSizer.Add(self.cancelBtn, 0, border=5, flag=wx.ALL | wx.EXPAND)
        
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.Add(self.dbPanel, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.controlSizer, 0, border=5, flag=wx.ALL | wx.EXPAND)

        self.SetSizer(self.mainSizer)
    
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1,
              size=wx.Size(400, 500), title='MySQL Configuration')
        
        self.__init_ctrls()
        self.__init_sizers()

        self.dbPanel.TransferDataToWindow()

    def OnOkButton(self, event):
        if self.dbPanel.Validate():
            configfile = open('wxpos.cfg', 'wb')
            if self.dbPanel.TransferDataFromWindow():
                config.write(configfile)
                self.Close()

class DatabaseConfigPanel(wx.Panel):
    def __init_ctrls(self):
        self.hostLbl = wx.StaticText(self, -1, label='Hostname')
        self.hostTxt = wx.TextCtrl(self, -1, validator=ConfigValidator('hostname'))

        self.portLbl = wx.StaticText(self, -1, label='Port')
        self.portTxt = wx.TextCtrl(self, -1, validator=ConfigValidator('port'))

        self.usernameLbl = wx.StaticText(self, -1, label='Username')
        self.usernameTxt = wx.TextCtrl(self, -1, validator=ConfigValidator('username'))

        self.passwordLbl = wx.StaticText(self, -1, label='Password')
        self.passwordTxt = wx.TextCtrl(self, -1,
                style=wx.TE_PASSWORD, validator=ConfigValidator('password'))

        self.dbNameLbl = wx.StaticText(self, -1, label='DB Name')
        self.dbNameTxt = wx.TextCtrl(self, -1, validator=ConfigValidator('db_name'))
    
    def __init_sizers(self):
        self.mainSizer = wx.FlexGridSizer(rows=6, cols=2)
        self.mainSizer.Add(self.hostLbl, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.hostTxt, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.portLbl, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.portTxt, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.usernameLbl, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.usernameTxt, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.passwordLbl, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.passwordTxt, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.dbNameLbl, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.dbNameTxt, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.mainSizer)
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        
        self.__init_ctrls()
        self.__init_sizers()

class ConfigValidator(wx.PyValidator):
    def __init__(self, key):
        wx.PyValidator.__init__(self)
        self.key = key

    Clone = lambda self: ConfigValidator(self.key)

    def Validate(self, parent):
        win = self.GetWindow()
        return True

    def TransferToWindow(self):
        try:
            win = self.GetWindow()
            try:
                data = config.get('MySQL', self.key)
            except:
                data = ''
            win.SetValue(data)
        except:
            print '-- ERROR -- in ConfigValidator.TransferToWindow'
            print '--', self.key
            raise
        return True

    def TransferFromWindow(self):
        try:
            win = self.GetWindow()
            config.set('MySQL', self.key, win.GetValue())
        except:
            print '-- ERROR -- in CoonfigValidator.TransferFromWindow'
            print '--', self.key
            raise
        return True
