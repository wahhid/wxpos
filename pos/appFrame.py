import wx

import pos

class AppFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, size=wx.Size(800, 600), title='App Frame')
        
        # Main toolbook that will contain all the modules' pages
        self.mainToolbook = wx.Toolbook(self, -1)
        self.actionToolbar = wx.ToolBar(self, -1, style=wx.TB_VERTICAL | wx.TB_BOTTOM)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_QUIT, size=(16, 16))
        quit_tool = self.actionToolbar.AddLabelTool(-1, 'Quit', bmp)
        self.Bind(wx.EVT_MENU, self.OnQuit, quit_tool)
        self.actionToolbar.Realize()
        
        # Simple sizer to stretch the content to fit the frame
        self.mainSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.mainSizer.Add(self.mainToolbook, 1, border=0, flag=wx.EXPAND | wx.ALL)
        self.mainSizer.Add(self.actionToolbar, 0, border=0, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(self.mainSizer)

        # Binding to fix a bug when closing the main frame
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_SHOW, self.OnShow)

    def OnShow(self, event):
        event.Skip()
        evt = pos.Event('app', pos.EVT_START)
        pos.event_queue.send(evt)

    def OnIdle(self, event):
        event.Skip()
        for evt in pos.event_queue.getall():
            for mod in pos.modules.all():
                if not mod.handle_event(evt):
                    break

    def OnQuit(self, event):
        event.Skip()
        self.Close()

    def OnCtrlTabCommand(self, event):
        """ Not used anymore. Was used with accelerator tables to switch between pages with keyboard."""
        event.Skip()
        sel = self.mainToolbook.GetSelection()
        pages = self.mainToolbook.GetPageCount()
        self.mainToolbook.ChangeSelection((sel+1)%pages)

    def OnCtrlShiftTabCommand(self, event):
        """ Not used anymore. Was used with accelerator tables to switch between pages with keyboard."""
        event.Skip()
        sel = self.mainToolbook.GetSelection()
        pages = self.mainToolbook.GetPageCount()
        self.mainToolbook.ChangeSelection((sel-1)%pages)

    def OnClose(self, event):
        """
        Close event handler to fix a problem when closing the application. (on Windows)
        Without it, the main frame freezes when closed.
        """
        pos.app.main.Exit()
    
    def loadMenu(self):
        """
        Load the menu "root" items and "items" into the toolbook with the appropriate pages. 
        """
        show_empty_root_items = pos.config['menu', 'show_empty_root_items']
        show_disabled_items = pos.config['menu', 'show_disabled_items']
        self.mainToolbook.AssignImageList(pos.menu.il)
        
        for root in pos.menu.main.items:
            if not root.enabled and not show_disabled_items:
                continue
            enabled_children = [i for i in root.children if i.enabled]
            if show_disabled_items:
                children = root.children
            else:
                children = enabled_children
            # Hide empty menu root items
            if len(children) == 0 and not show_empty_root_items:
                continue
            page = self.getToolbookPage(children)
            self.mainToolbook.AddPage(imageId=root.image, page=page, select=False, text=root.label)
            page.Enable(root.enabled)# and len(enabled_children) != 0)

    def getToolbookPage(self, items):
        """
        Returns the appropriate window to be placed in the main Toolbook depending on the items of a root menu item.
        """
        count = len(items)
        if count == 0:
            page = wx.Panel(self.mainToolbook, -1)
            page.Enable(False)
            return page
        elif count == 1:
            page = items[0].page(self.mainToolbook)
            page.Enable(items[0].enabled)
            return page
        else:
            toolbook = wx.Toolbook(self.mainToolbook, -1)
            toolbook.AssignImageList(pos.menu.il)

            for item in items:
                page = item.page(toolbook)
                toolbook.AddPage(imageId=item.image, page=page, select=False, text=item.label)
                page.Enable(item.enabled)
            return toolbook
