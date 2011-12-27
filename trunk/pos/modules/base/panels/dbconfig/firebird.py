import wx

from .base import DatabaseConfigPanel

class FirebirdConfigPanel(DatabaseConfigPanel):
    def __init__(self, parent):
        DatabaseConfigPanel.__init__(self, parent, 'db.firebird')
        
        self.addParam('host', 'Host', wx.TextCtrl, required=False)
        self.addParam('port', 'Port', wx.TextCtrl, required=False)
        self.addParam('username', 'User', wx.TextCtrl, required=False)
        self.addParam('password', 'Password', wx.TextCtrl, required=False,
                      style=wx.TE_PASSWORD)
        self.addParam('database', 'Filename', wx.TextCtrl, required=True)
        self.placeParam()
