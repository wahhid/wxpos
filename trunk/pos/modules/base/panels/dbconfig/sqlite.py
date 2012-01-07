import wx

from .base import DatabaseConfigPanel

class SqliteConfigPanel(DatabaseConfigPanel):
    def __init__(self, parent, getProfile):
        DatabaseConfigPanel.__init__(self, parent, getProfile)
        
        self.addParam('database', 'Filename', wx.TextCtrl, required=False)
        self.placeParam()
