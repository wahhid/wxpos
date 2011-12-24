import wx

import pos

import pos.menu

import pos.modules

class AppFrame(wx.Frame):
    def _init_sizers(self):
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.AddWindow(self.mainToolbook, 1, border=0, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(self.mainSizer)

    def _init_main(self):
        self.mainToolbook = wx.Toolbook(self, -1)

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1,
                size=wx.Size(800, 600), title='App Frame')
        
        self._init_main()
        self._init_sizers()

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnCtrlTabCommand(self, event):
        """ Not used anymore. Was used with accelerator tables."""
        event.Skip()
        sel = self.mainToolbook.GetSelection()
        pages = self.mainToolbook.GetPageCount()
        self.mainToolbook.ChangeSelection((sel+1)%pages)

    def OnCtrlShiftTabCommand(self, event):
        """ Not used anymore. Was used with accelerator tables."""
        event.Skip()
        sel = self.mainToolbook.GetSelection()
        pages = self.mainToolbook.GetPageCount()
        self.mainToolbook.ChangeSelection((sel-1)%pages)

    def OnClose(self, event):
        pos.app.app.Exit()
        #event.Skip()
    
    def loadMenu(self):
        self.mainToolbook.AssignImageList(pos.menu.il)
        # TODO arrange the permission-menu relation, change the whole permission system
        if pos.modules.isInstalled('user'):
            import pos.modules.user.objects.user as user
            for item in pos.menu.getItems():
                current_role = user.current.role
                if current_role.isPermitted(item.perm):
                    children = []
                    for i in item.children:
                        if current_role.isPermitted(i.perm):
                            children.append(i)
                    page = self.getToolbookPage(children)
                    self.mainToolbook.AddPage(imageId=item.image, page=page, select=False, text=item.label)
        else:
            for item in pos.menu.getItems():
                children = []
                for i in item.children:
                    children.append(i)
                page = self.getToolbookPage(children)
                self.mainToolbook.AddPage(imageId=item.image, page=page, select=False, text=item.label)


    def getToolbookPage(self, items):
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
