print '-- APP INIT --'

import sys
print '*Python', sys.version, 'on', sys.platform

import wx
print '*Running on wxPython', wx.version()

import ConfigParser

import pos

pos.config = ConfigParser.SafeConfigParser()
pos.config.read('wxpos.cfg')

print '*Creating IdManager...'
import pos.modules.base.objects.idManager as idManager
idManager.init()

print '*Creating menu...'
import pos.menu
pos.menu.init()

print '*Importing modules...'
import pos.modules

print '*Importing database...'
import pos.database

class PosApp(wx.App):
    def __init__(self, config, redirect):
        self.config = config
        wx.App.__init__(self, redirect=redirect)
        
    def OnInit(self):
        if self.config or len(pos.config.sections()) == 0:
            return self.runConfig()
        else:
            return self.runApp()

    def runApp(self):
        print '*Creating database...'
        pos.db = pos.database.DB()
        
        print '*Importing app frame'
        from pos.appFrame import AppFrame
        
        print '*Extending menu...'
        pos.modules.extendMenu(pos.menu.menu)
        print '*Loading menu...'
        pos.menu.load()
        print '*Initiating App...'
        if pos.modules.isInstalled('user'):
            print '*Module installed user'
            print '*Login required'
            if not self.requireLogin():
                return False
        self.main = AppFrame(None)
        self.main.loadMenu()
        print '*Done.'
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

    def requireLogin(self):
        from pos.modules.user.dialogs.loginDialog import LoginDialog
        login = LoginDialog(None)
        result = login.ShowModal()
        return (result == wx.ID_OK)

    def runConfig(self):
        wx.MessageBox('''No configuration file detected. Please run wxpos-config.
Configuration frame not done yet.''',
                      'First Run',
                      style=wx.OK | wx.ICON_INFORMATION)
        return False

def run(config=False):
    global app
    print '*Creating App instance...'
    app = PosApp(config, redirect=False)
    app.MainLoop()
