print '-- CONFIG INIT --'

import pos

import sys
import wx

print '*Creating database...'
import pos.database

print '*Importing modules...'
import pos.modules

base_mod = pos.mod.base
ConfigDialog = base_mod.dialogs.dbconfig.ConfigDialog
from pos.modules.base.dialogs.dbconfig import ConfigDialog

def run():
    global pos
    app = wx.PySimpleApp()
    dlg = ConfigDialog(None)
    dlg.ShowModal()
    pos.database.start()
    
    retCode = wx.MessageBox('Reconfigure Database?\nThis will drop the database you chose and recreate it.', 'Database config', style=wx.YES_NO | wx.ICON_QUESTION)
    reset = (retCode == wx.YES)
    if not reset:
        return
    print '*Configuring database...'
    pos.modules.configDB()
    retCode = wx.MessageBox('Insert Test Values?', 'Database config', style=wx.YES_NO | wx.ICON_QUESTION)
    test = (retCode == wx.YES)
    print '*Test values %s...' % ('on' if test else 'off',)
    pos.modules.configTestDB()
