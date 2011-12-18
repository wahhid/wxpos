print '-- APP INIT --'

import sys
print '*Python', sys.version, 'on', sys.platform

import wx
print '*Running on wxPython', wx.version()

import pos

print '*Creating menu...'
import pos.menu
pos.menu.init()

print '*Importing database...'
import pos.database
pos.database.init()

print '*Importing modules...'
import pos.modules
pos.modules.init()

print '*Creating IdManager...'
from pos.modules.base.objects import idManager
idManager.init()

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
        from pos.modules.user.dialogs import LoginDialog
        login = LoginDialog(None)
        result = login.ShowModal()
        return (result == wx.ID_OK)

    def runConfig(self):
        from pos.modules.base.dialogs.dbconfig import ConfigDialog
        dlg = ConfigDialog(None)
        retCode = dlg.ShowModal()
        cont = (retCode == wx.ID_OK)
        if not cont:
            return False
        
        print '*Restarting database...'
        pos.database.restart()
        
        retCode = wx.MessageBox('Reconfigure Database?\nThis will drop the database you chose and recreate it.', 'Database config', style=wx.YES_NO | wx.ICON_QUESTION)
        reset = (retCode == wx.YES)
        if not reset:
            return False
        print '*Configuring database...'
        pos.modules.configDB()
        retCode = wx.MessageBox('Insert Test Values?', 'Database config', style=wx.YES_NO | wx.ICON_QUESTION)
        test = (retCode == wx.YES)
        print '*Test values are %s...' % ('on' if test else 'off',)
        if test:
            pos.modules.configTestDB()
        print '*Done.'
        return False

def run(config=False):
    global app
    print '*Creating App instance...'
    app = PosApp(config, redirect=False)
    app.MainLoop()
