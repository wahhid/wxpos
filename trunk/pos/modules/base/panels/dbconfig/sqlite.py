import wx

from .base import DatabaseConfigPanel

class SqliteConfigPanel(DatabaseConfigPanel):
    def __init__(self, parent):
        DatabaseConfigPanel.__init__(self, parent, 'db.sqlite')
        
        self.addParam('database', 'Filename', wx.TextCtrl, required=False)
        self.placeParam()
