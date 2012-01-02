import wx

import pos

class AppFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, size=wx.Size(800, 600), title='App Frame')
        
        # Main toolbook that will contain all the modules' pages
        self.mainToolbook = wx.Toolbook(self, -1)
        # Simple sizer to stretch the content to fit the frame
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.AddWindow(self.mainToolbook, 1, border=0, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(self.mainSizer)

        # Binding to fix a bug when closing the main frame
        self.Bind(wx.EVT_CLOSE, self.OnClose)

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
        pos.app.app.Exit()
    
    def loadMenu(self):
        """
        Load the menu "root" items and "items" into the toolbook with the appropriate pages. 
        """
        self.mainToolbook.AssignImageList(pos.menu.il)
        if pos.modules.isInstalled('user'):
            import pos.modules.user.objects.user as user
            from pos.modules.user.objects.superuser import SuperUser
            
            if isinstance(user.current, SuperUser):
                # Ignore permissions if logged in as "superuser"
                self._loadCompleteMenu()
            else:
                restrictions = [(mr.root, mr.item) for mr in user.current.menu_restrictions] 
                for item in pos.menu.main.getItems():
                    # Filter menu items to display according to permissions
                    children = [i for i in item.children if (item.label, i.label) in restrictions]
                    # Hide empty menu root items
                    if len(children) == 0: continue
                    page = self.getToolbookPage(children)
                    self.mainToolbook.AddPage(imageId=item.image, page=page, select=False, text=item.label)
        else:
            self._loadCompleteMenu()
        
    def _loadCompleteMenu(self):
        """
        Load the complete menu into the main toolbook, ignoring any permissions set.
        """
        for item in pos.menu.main.getItems():
            page = self.getToolbookPage(item.children)
            self.mainToolbook.AddPage(imageId=item.image, page=page, select=False, text=item.label)

    def getToolbookPage(self, items):
        """
        Returns the appropriate window to be placed in the main Toolbook depending on the items of a root menu item.
        """
        count = len(items)
        if count == 0:
            return wx.Panel(self.mainToolbook, -1)
        elif count == 1:
            return items[0].page(self.mainToolbook)
        else:
            toolbook = wx.Toolbook(self.mainToolbook, -1)
            toolbook.AssignImageList(pos.menu.il)

            for item in items:
                toolbook.AddPage(imageId=item.image, page=item.page(toolbook), select=False, text=item.label)
            return toolbook
