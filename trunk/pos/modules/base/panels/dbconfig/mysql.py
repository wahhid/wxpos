import wx

from .base import DatabaseConfigPanel

class MySQLConfigPanel(DatabaseConfigPanel):
    def __init__(self, parent, getProfile):
        DatabaseConfigPanel.__init__(self, parent, getProfile)
        
        self.addParam('host', 'Host', wx.TextCtrl, required=True)
        self.addParam('port', 'Port', wx.TextCtrl, required=False)
        self.addParam('username', 'Username', wx.TextCtrl, required=False)
        self.addParam('password', 'Password', wx.TextCtrl, required=False,
                      style=wx.TE_PASSWORD)
        self.addParam('database', 'Database', wx.TextCtrl, required=True)
        self.placeParam()
