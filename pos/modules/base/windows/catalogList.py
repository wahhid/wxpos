import wx

class CatalogList(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_ICON | wx.LC_AUTOARRANGE | wx.LC_SINGLE_SEL)
        
        il = wx.ImageList(32,32, True)
        
        folder_bmp = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, size=(32, 32))
        file_bmp = wx.ArtProvider.GetBitmap(wx.ART_HELP_BOOK, size=(32, 32))
        up_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DIR_UP, size=(32, 32))
        
        il.Add(folder_bmp)
        il.Add(file_bmp)
        il.Add(up_bmp)

        self.AssignImageList(il, wx.IMAGE_LIST_NORMAL)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivate)

        self.__tree = []
        self.__view = []
        self.__current = None
        self.updateList(None)

    def getItem(self, index):
        return self.__view[index]

    def clearCatalog(self):
        self.DeleteAllItems()
        self.__view = []

    def OnItemActivate(self, event):
        event.Skip()
        selected = self.GetFirstSelected()
        item, image_id = self.getItem(selected)
        if item is None and image_id == 2:
            if len(self.__tree) == 0:
                parent = None
            else:
                parent = self.__tree.pop()
            self.updateList(parent)
        elif image_id == 0:
            if self.__current is not None:
                self.__tree.append(self.__current)
            self.updateList(item)
        elif image_id == 3:
            if self.__current is not None:
                self.__tree.append(self.__current)
            self.updateList('All')

    def getChildren(self, parent):
        return [[], []]

    def updateList(self, parent):
        self.__current = parent
        if parent == 'All':
            children = [[], self.getAll()]
        else:
            children = self.getChildren(parent)

        self.clearCatalog()
        _last_index = -1
        if parent is None:
            _last_index += 1
            self.InsertImageStringItem(_last_index, '[All]', 0)
            self.__view.append((None, 3))
        else:
            _last_index += 1
            self.InsertImageStringItem(_last_index, '[Up]', 2)
            self.__view.append((None, 2))
        for image_id, items in enumerate(children):
            for (item, disp) in items:
                _last_index += 1
                self.InsertImageStringItem(_last_index, disp, image_id)
                self.__view.append((item, image_id))
