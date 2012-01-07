import wx

import pos

from ..panels import FirebirdConfigPanel, MsSQLConfigPanel, PostgreSQLConfigPanel, MySQLConfigPanel, SqliteConfigPanel

class ConfigDialog(wx.Dialog):
    def __init_ctrls(self):
        intro_txt = 'Select and configure the database system you want to use.\nNote: wxPos will not create the database for you.'
        self.introTxt = wx.StaticText(self, -1, label=intro_txt)
        
        self.profileChoice = wx.Choice(self, -1)
        self.profileChoice.Bind(wx.EVT_CHOICE, self.OnProfileChoice)
        
        self.addProfileBtn = wx.Button(self, -1, '+')
        self.addProfileBtn.Bind(wx.EVT_BUTTON, self.OnAddButton)
        self.removeProfileBtn = wx.Button(self, -1, '-')
        self.removeProfileBtn.Bind(wx.EVT_BUTTON, self.OnRemoveButton)
        
        self.nameTxt = wx.TextCtrl(self, -1)
        
        self.panelBook = wx.Choicebook(self, -1)
        self.addOption('sqlite', 'Sqlite', SqliteConfigPanel(self.panelBook, self.getProfile))
        self.addOption('mysql', 'MySQL', MySQLConfigPanel(self.panelBook, self.getProfile))
        self.addOption('postgresql', 'PostgreSQL', PostgreSQLConfigPanel(self.panelBook, self.getProfile))
        self.addOption('mssql', 'Microsoft SQL Server', MsSQLConfigPanel(self.panelBook, self.getProfile))
        self.addOption('firebird', 'Firebird', FirebirdConfigPanel(self.panelBook, self.getProfile))
        
        self.okBtn = wx.Button(self, wx.ID_OK, label='OK')
        self.okBtn.Bind(wx.EVT_BUTTON, self.OnOkButton)

        self.cancelBtn = wx.Button(self, wx.ID_CANCEL, label='Cancel')
    
    def __init_sizers(self):
        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlSizer.Add(self.okBtn, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.controlSizer.Add(self.cancelBtn, 0, border=5, flag=wx.ALL | wx.EXPAND)
        
        self.profileSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.profileSizer.Add(self.profileChoice, 1, flag=wx.EXPAND | wx.ALL)
        self.profileSizer.Add(self.addProfileBtn, 0, border=5, flag=wx.RIGHT | wx.LEFT)
        self.profileSizer.Add(self.removeProfileBtn, 0, border=5, flag=wx.RIGHT | wx.LEFT)
        
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.Add(self.introTxt, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.profileSizer, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.nameTxt, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.panelBook, 1, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.controlSizer, 0, border=5, flag=wx.ALL | wx.EXPAND)

        self.SetSizer(self.mainSizer)
    
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1,
              size=wx.Size(400, 500), title='Database Configuration')

        self.options = []
        
        self.__init_ctrls()
        self.__init_sizers()
        
        self.profiles = [section_name[3:] for section_name, s in pos.config if section_name.startswith('db.')]
        if 'default' not in self.profiles:
            self.profiles.append('default')
        self.profileChoice.SetItems(self.profiles)
        
        self.setProfile(pos.config['db', 'used'])
        self.profileChoice.SetStringSelection(self.profile)

    def addOption(self, name, label, panel):
        self.panelBook.AddPage(panel, label)
        self.options.append(name)

    def getProfile(self):
        return self.profile

    def setProfile(self, profile):
        self.profile = profile
        
        self.removeProfileBtn.Enable(self.profile != 'default')
        
        self.nameTxt.SetValue(self.profile)
        self.nameTxt.Enable(self.profile != 'default')
        
        drivername = pos.config['db.'+self.profile, 'drivername']
        index = self.options.index(drivername) if drivername is not None else 0
        
        self.panelBook.SetSelection(index)
        self.panelBook.Enable(self.profile != 'default')
        
        for i in range(self.panelBook.GetPageCount()):
            panel = self.panelBook.GetPage(i)
            panel.TransferDataToWindow()

    def OnProfileChoice(self, event):
        event.Skip()
        self.setProfile(self.profileChoice.GetStringSelection())

    def OnAddButton(self, event):
        event.Skip()
        i = 0
        profile = 'profile%d' % (i,)
        while profile in self.profiles:
            i += 1
            profile = 'profile%d' % (i,)
        self.profiles.append(profile)
        
        self.profileChoice.SetItems(self.profiles)
        pos.config['db.'+profile] = pos.config['db.default']
        self.setProfile(profile)
        
        self.profileChoice.SetStringSelection(self.profile)

    def OnRemoveButton(self, event):
        event.Skip()
        profile = self.profileChoice.GetStringSelection()
        
        self.profiles.remove(profile)
        self.profileChoice.SetItems(self.profiles)
        pos.config['db.'+profile] = None
        self.setProfile('default')
        
        self.profileChoice.SetStringSelection(self.profile)

    def OnOkButton(self, event):
        profile = self.nameTxt.GetValue()
        if profile != self.profile and profile in self.profiles: return
        
        pos.config['db.'+self.profile] = None
        self.profile = profile    
        
        drivername_index = self.panelBook.GetSelection()
        drivername = self.options[drivername_index]
        
        index = self.panelBook.GetSelection()
        panel = self.panelBook.GetPage(index)
        if panel.Validate():
            pos.config['db.'+self.profile] = {'drivername': drivername}
            if panel.TransferDataFromWindow():
                pos.database.config.use(self.profile)
                pos.config.save()
                event.Skip()
