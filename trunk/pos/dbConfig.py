print '-- CONFIG INIT --'

import pos

import wx

print '*Creating database...'
import pos.database
pos.db = pos.database.DB()

print '*Importing modules...'
import pos.modules

def run():
    if not pos.db.isConnected():
        print '*Database connection error.'
        print '*Aborting...'
    else:
        app = wx.PySimpleApp()
        retCode = wx.MessageBox('Insert Test Values?', 'Database config', style=wx.YES_NO | wx.ICON_QUESTION)
        app.MainLoop()
        test = (retCode == wx.YES)
        print '*Configuring database...'
        print '*Test values %s...' % ('on' if test else 'off',)
        pos.modules.configDB(test)

if __name__ == '__main__':
    run()
