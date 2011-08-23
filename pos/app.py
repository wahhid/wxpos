print '-- APP INIT --'

import wx

print '*Creating database...'
import pos.db
pos.db.db = pos.db.DB()

print '*Creating IdManager...'
import pos.modules.base.objects.idManager as idManager
idManager.init()

print '*Creating menu...'
import pos.menu
pos.menu.init()

print '*Importing modules...'
import pos.modules
print '*Extending database...'
pos.modules.extendDB(pos.db.db)
print '*Extending menu...'
pos.modules.extendMenu(pos.menu.menu)

print '*Importing login dialog'
import pos.loginDialog
print '*Importing app frame'
import pos.appFrame

class PosApp(wx.App):
    def OnInit(self):
        print '*Loading menu...'
        pos.menu.load()
        print '*Initiating App...'
        if not self.requireLogin():
            return False
        self.main = pos.appFrame.create(None)
        print '*Done.'
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

    def requireLogin(self):
        login = pos.loginDialog.create(None)
        result = login.ShowModal()
        return (result == wx.ID_OK)

app = None
def run():
    global app
    app = PosApp(redirect=False)
    app.MainLoop()

if __name__ == '__main__':
    run()
