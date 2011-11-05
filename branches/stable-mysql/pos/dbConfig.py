print '-- CONFIG INIT --'

import pos

import wx

print '*Creating database...'
import pos.database

print '*Importing modules...'
import pos.modules

from pos.modules.base.dialogs.dbconfig import ConfigDialog

def run():
    app = wx.PySimpleApp()
    dlg = ConfigDialog(None)
    dlg.ShowModal()
    pos.db = pos.database.DB()
    if not pos.db.isConnected():
        print '*Database connection error.'
        print '*Aborting...'
    else:
        retCode = wx.MessageBox('Reconfigure Database?\nThis will drop the database you chose and recreate it.', 'Database config', style=wx.YES_NO | wx.ICON_QUESTION)
        reset = (retCode == wx.YES)
        if not reset:
            return
        retCode = wx.MessageBox('Insert Test Values?', 'Database config', style=wx.YES_NO | wx.ICON_QUESTION)
        test = (retCode == wx.YES)
        print '*Configuring database...'
        print '*Test values %s...' % ('on' if test else 'off',)
        pos.modules.configDB(test)
