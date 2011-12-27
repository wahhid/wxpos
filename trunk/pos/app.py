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

print '*Importing modules...'
import pos.modules
pos.modules.init()

def runApp():
    print '*Starting database...'
    try:
        pos.database.init()
    except Exception as e:
        wx.MessageBox('Could not connect to database:\n%s' % (e,), 'Database error', style=wx.ICON_ERROR | wx.OK)
        return False
    pos.modules.loadDB()
    
    print '*Importing app frame'
    from pos.appFrame import AppFrame
    
    print '*Extending menu...'
    pos.modules.extendMenu(pos.menu.menu)
    print '*Loading menu...'
    pos.menu.load()
    print '*Initiating App...'
    for mod in pos.modules.all():
        init = mod.init()
        if init is not None and not init:
            print '*Initiating module', mod.name, 'failed.'
            return False
    main = AppFrame(None)
    main.loadMenu()
    print '*Done.'
    app.SetTopWindow(main)
    main.Show()
    return True

def runConfig():
    from pos.modules.base.dialogs.dbconfig import ConfigDialog
    dlg = ConfigDialog(None)
    app.SetTopWindow(dlg)
    retCode = dlg.ShowModal()
    cont = (retCode == wx.ID_OK)
    if not cont:
        return False
    
    print '*Starting database...'
    try:
        pos.database.init()
    except Exception as e:
        wx.MessageBox('Could not connect to database:\n%s' % (e,), 'Database error', style=wx.ICON_ERROR | wx.OK)
        return False
    pos.modules.loadDB()
    
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

app = None
def run(config=False):
    global app
    print '*Creating App instance...'
    app = wx.App(redirect=False)
    if config:
        print '*Running config...'
        ret = runConfig()
    elif pos.config.empty():
        print '*First run. Running config first...'
        ret = runConfig()
        ret = ret or runApp()
    else:
        print '*Running app...'
        ret = runApp()
    if ret: app.MainLoop()
