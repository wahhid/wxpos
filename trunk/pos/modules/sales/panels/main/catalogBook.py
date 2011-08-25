import wx

import pos.modules.customer.objects.customer as customer
import pos.modules.customer.objects.customergroup as customergroup

import pos.modules.stock.objects.category as category
import pos.modules.stock.objects.product as product

from pos.modules.base.objects.idManager import ids

class CatalogBook(wx.Toolbook):
    def __init__(self, parent):
        wx.Toolbook.__init__(self, parent, -1, style=wx.BK_LEFT)

        il = wx.ImageList(24,24, True)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DIR_UP, size=(24, 24))
        il.Add(bmp)
        self.AssignImageList(il)
        
        self.productList = ProductCatalogList(self)
        self.AddPage(imageId=0, page=self.productList, text='Products')
        
        self.customerList = CustomerCatalogList(self)
        self.AddPage(imageId=0, page=self.customerList, text='Customers')

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

    def getChildren(self, parent):
        return [[], []]

    def updateList(self, parent):
        self.__current = parent
        children = self.getChildren(parent)

        self.clearCatalog()
        _last_index = -1
        if parent is not None:
            _last_index += 1
            self.InsertImageStringItem(_last_index, '[Up]', 2)
            self.__view.append((None, 2))
        for image_id, items in enumerate(children):
            for (item, disp) in items:
                _last_index += 1
                self.InsertImageStringItem(_last_index, disp, image_id)
                self.__view.append((item, image_id))

class ProductCatalogList(CatalogList):
    def getChildren(self, parent):
        children_categories = category.find(list=True, parent_category=parent)
        children_products = product.find(list=True, category=parent)

        return [map(lambda c: (c, c.data['name']), children_categories),
                map(lambda p: (p, p.data['name']), children_products)]

class CustomerCatalogList(CatalogList):
    def getChildren(self, parent):
        children_groups = customergroup.find(list=True) if parent is None else []

        customers = customer.find(list=True)
        children_customers = filter(lambda c: parent in c.data['groups'], customers)

        return [map(lambda cg: (cg, cg.data['name']), children_groups),
                map(lambda c: (c, c.data['name']), children_customers)]
