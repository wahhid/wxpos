print '-- APP INIT --'

import sys
print '*Python', sys.version, 'on', sys.platform

import wx
print '*Running on wxPython', wx.version()

import pos

pos.config.set_default('app', 'fullscreen', '')
pos.config.set_default('app', 'first_run', '1')
pos.config.set_default('app', 'pos_id', '0')

print '*Creating menu...'
import pos.menu
pos.menu.init()

print '*Importing database...'
import pos.database

print '*Importing modules...'
import pos.modules
pos.modules.init()

def goTo(root, item=None):
    root_index, item_index = 0, 0
    mainToolbook = main.frame.mainToolbook
    for i in xrange(mainToolbook.GetPageCount()):
        if mainToolbook.GetPageText(i) == root:
            root_index = i
            break
    else:
        return
    root_page = mainToolbook.GetPage(root_index)
    mainToolbook.SetSelection(root_index)
    if isinstance(root_page, wx.Toolbook) and item is not None:
        for i in xrange(root_page.GetPageCount()):
            if root_page.GetPageText(i) == item:
                item_index = i
                break
        else:
            return
        root_page.SetSelection(item_index)

def runApp():
    """
    Run application in normal mode.
    The main application frame is shown if all the modules load successfully.
    """
    print '*Starting database...'
    try:
        pos.database.init()
    except Exception as e:
        wx.MessageBox('Could not connect to database:\n%s' % (e,), 'Database error', style=wx.ICON_ERROR | wx.OK)
        return False
    # Load database objects of every module
    pos.modules.loadDB()
    
    print '*Importing app frame'
    from pos.appFrame import AppFrame
    
    print '*Extending menu...'
    # Load appropriate menu items from all the modules
    pos.modules.extendMenu(pos.menu.main)
    print '*Loading menu...'
    # Create the image list once the wx.App is created and the menu fully extended
    pos.menu.load()
    print '*Initiating App...'
    # Initiate every installed module
    for mod in pos.modules.all():
        init = mod.init()
        if init is not None and not init:
            print '*Initiating module', mod.name, 'failed.'
            return False
    main.frame = AppFrame(None)
    main.frame.loadMenu()
    print '*Done.'
    main.SetTopWindow(main.frame)
    if bool(pos.config['app', 'fullscreen']):
        main.frame.ShowFullScreen(True, style=wx.FULLSCREEN_NOBORDER)
    else:
        main.frame.Show()
    return True

def runConfig():
    """
    Run application in configuration mode.
    Change database configuration and create/clear database structure.
    """
    # Prompt the user to change database configuration
    from pos.modules.base.dialogs.dbconfig import ConfigDialog
    dlg = ConfigDialog(None)
    main.SetTopWindow(dlg)
    retCode = dlg.ShowModal()
    cont = (retCode == wx.ID_OK)
    if not cont:
        return False
    
    # Start the database AFTER potential changes in the configuration 
    print '*Starting database...'
    try:
        pos.database.init()
    except Exception as e:
        wx.MessageBox('Could not connect to database:\n%s' % (e,), 'Database error', style=wx.ICON_ERROR | wx.OK)
        return False
    # Load database objects of every module
    pos.modules.loadDB()
    
    # Prompt the user to completely flush the chosen database and recreate the structure
    retCode = wx.MessageBox('Reconfigure Database?\nThis will drop the database you chose and recreate it.', 'Database config', style=wx.YES_NO | wx.ICON_QUESTION)
    reset = (retCode == wx.YES)
    if not reset:
        return False
    print '*Configuring database...'
    pos.modules.configDB()
    
    # Prompt the user to add initial testing values, just to see it working immediately
    retCode = wx.MessageBox('Insert Test Values?', 'Database config', style=wx.YES_NO | wx.ICON_QUESTION)
    test = (retCode == wx.YES)
    print '*Test values are %s...' % ('on' if test else 'off',)
    if test:
        pos.modules.configTestDB()
    print '*Done.'
    return False

main = None
def run(config=False):
    """
    Main function to run the application.
    The config parameter specifies which mode to run the application in.
    """
    global main
    print '*Creating App instance...'
    main = wx.App(redirect=False)
    if pos.config['app', 'first_run'] or pos.config.empty():
        pos.config['app', 'first_run'] = ''
        # Force configuration if no configuration file is present.
        pos.config.save_defaults(overwrite=False)
        print '*First run. Running config first...'
        ret = runConfig()
        ret = ret or runApp()
    elif config:
        print '*Running config...'
        ret = runConfig()
    else:
        print '*Running app...'
        ret = runApp()
    # Run main loop only if a frame is persistently present.
    # It is not the case when the application is in configuration mode or 
    # modules' init() function return False for example.
    if ret: main.MainLoop()
