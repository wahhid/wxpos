import wx

class Catalog(wx.PyPanel):
    def __init__(self, parent,
                 folder_bmp=None, file_bmp=None, up_bmp=None, all_bmp=None,
                 show_all_item=True, show_search_box=True):
        wx.PyPanel.__init__(self, parent, -1)
        
        self.show_search_box = show_search_box
        
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        if self.show_search_box:
            self.searchTxt = wx.SearchCtrl(self, -1)
            self.searchTxt.Bind(wx.EVT_TEXT, self.OnSearchText)
            self.sizer.Add(self.searchTxt, 0, border=5, flag=wx.EXPAND | wx.RIGHT | wx.LEFT)
        
        self.list = CatalogList(self, folder_bmp, file_bmp, up_bmp, all_bmp, show_all_item)
        self.list.updateList(None)
        self.sizer.Add(self.list, 1, border=5, flag=wx.EXPAND | wx.ALL)
        
        self.SetSizer(self.sizer)
    
    def OnSearchText(self, event):
        event.Skip()
        value = self.searchTxt.GetValue()
        wx.CallLater(500, self._doSearch, value)

    def _doSearch(self, old_value):
        value = self.searchTxt.GetValue()
        if old_value != value: return
        if value == '': value = None
        self.list.updateList(None, search=value)
            

    def GetValue(self):
        return self.list.GetValue()

    def getChildren(self, parent):
        return [[], []]
    
    def getAll(self, search=None):
        return []

class CatalogList(wx.ListCtrl):
    def __init__(self, parent,
                 folder_bmp=None, file_bmp=None, up_bmp=None, all_bmp=None,
                 show_all_item=True):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_ICON | wx.LC_AUTOARRANGE | wx.LC_SINGLE_SEL)
        
        il = wx.ImageList(32,32, True)

        if folder_bmp is None:
            folder_bmp = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, size=(32, 32))
        if file_bmp is None:
            file_bmp = wx.ArtProvider.GetBitmap(wx.ART_HELP_BOOK, size=(32, 32))
        if up_bmp is None:
            up_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DIR_UP, size=(32, 32))
        if all_bmp is None:
            all_bmp = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, size=(32, 32))
        
        il.Add(folder_bmp)
        il.Add(file_bmp)
        il.Add(up_bmp)
        il.Add(all_bmp)

        self.AssignImageList(il, wx.IMAGE_LIST_NORMAL)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivate)

        self.parent = parent
        self.show_all_item = show_all_item
        self.__tree = []
        self.__view = []
        self.__current = None
        self.updateList(None)

    def GetValue(self):
        selected = self.GetFirstSelected()
        item, image_id = self.getItem(selected)
        if image_id == 1:
            return item
        else:
            return None

    def getItem(self, index):
        if index<0:
            return None, None
        else:
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

    def updateList(self, parent, search=None):
        self.__current = parent
        if parent == 'All' or search is not None:
            children = [[], self.getAll(search)]
        else:
            children = self.getChildren(parent)

        self.clearCatalog()
        _last_index = -1
        if search is None:
            if parent is None and self.show_all_item:
                _last_index += 1
                self.InsertImageStringItem(_last_index, '[All]', 3)
                self.__view.append((None, 3))
            elif parent is not None:
                _last_index += 1
                self.InsertImageStringItem(_last_index, '[Up]', 2)
                self.__view.append((None, 2))
        for image_id, items in enumerate(children):
            for (item, disp) in items:
                _last_index += 1
                self.InsertImageStringItem(_last_index, disp, image_id)
                self.__view.append((item, image_id))

    def getChildren(self, parent):
        return self.parent.getChildren(parent)
    
    def getAll(self, search=None):
        return self.parent.getAll(search)
