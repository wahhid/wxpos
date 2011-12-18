import wx

import pos

import pos.menu

from pos.modules.base.objects.idManager import ids

import pos.modules
if pos.modules.isInstalled('user'):
    import pos.modules.user.objects.user as user
    from pos.modules.user.objects.permission import Permission

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

        accTable = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, wx.WXK_TAB, ids['CtrlTab']),
            (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, wx.WXK_TAB, ids['CtrlShiftTab'])])
        self.Bind(wx.EVT_MENU, self.OnCtrlTabCommand, id=ids['CtrlTab'])
        self.Bind(wx.EVT_MENU, self.OnCtrlShiftTabCommand, id=ids['CtrlShiftTab']) 
        self.SetAcceleratorTable(accTable)
        
        self._init_main()
        self._init_sizers()

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnCtrlTabCommand(self, event):
        event.Skip()
        sel = self.mainToolbook.GetSelection()
        pages = self.mainToolbook.GetPageCount()
        self.mainToolbook.ChangeSelection((sel+1)%pages)

    def OnCtrlShiftTabCommand(self, event):
        event.Skip()
        sel = self.mainToolbook.GetSelection()
        pages = self.mainToolbook.GetPageCount()
        self.mainToolbook.ChangeSelection((sel-1)%pages)

    def OnClose(self, event):
        pos.app.app.Exit()
        #event.Skip()
    
    def loadMenu(self):
        self.mainToolbook.AssignImageList(pos.menu.il)
        if pos.modules.isInstalled('user'):
            for item in pos.menu.getItems():
                current_role = user.current.role
                session = pos.database.session()
                # TODO arrange that query
                permission_in_role = session.query(Permission).filter((Permission.name == item.perm) & \
                                                                      Permission.roles.contains(user.current.role))
                if item.perm is None or permission_in_role.count() == 1:
                    children = []
                    for i in item.children:
                        permission_in_role = session.query(Permission).filter((Permission.name == i.perm) & \
                                                                              Permission.roles.contains(user.current.role))
                        if i.perm is None or permission_in_role.count() == 1:
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
