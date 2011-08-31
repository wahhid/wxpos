print '-- APP INIT --'

import wx

import pos

print '*Creating database...'
import pos.database
pos.db = pos.database.DB()

print '*Creating IdManager...'
import pos.modules.base.objects.idManager as idManager
idManager.init()

print '*Creating menu...'
import pos.menu
pos.menu.init()

print '*Importing modules...'
import pos.modules
print '*Extending menu...'
pos.modules.extendMenu(pos.menu.menu)

print '*Importing app frame'
from pos.appFrame import AppFrame

class PosApp(wx.App):
    def OnInit(self):
        print '*Loading menu...'
        pos.menu.load()
        print '*Initiating App...'
        if pos.modules.isInstalled('user'):
            print '*Module installed user'
            print '*Login required'
            if not self.requireLogin():
                return False
        self.main = AppFrame(None)
        print '*Done.'
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

    def requireLogin(self):
        from pos.modules.user.dialogs.loginDialog import LoginDialog
        login = LoginDialog(None)
        result = login.ShowModal()
        return (result == wx.ID_OK)

app = None
def run():
    global app
    app = PosApp(redirect=False)
    app.MainLoop()

if __name__ == '__main__':
    run()
