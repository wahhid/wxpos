import wx

import pos.modules.user.objects.user as user

from pos.modules.base.windows.catalogList import CatalogList

class UserCatalogList(CatalogList):
    def __init__(self, parent):
        CatalogList.__init__(self, parent,
                             file_bmp=wx.Bitmap('images/user.png', wx.BITMAP_TYPE_PNG),
                             show_all_item=False)
    
    def getAll(self):
        users = user.find(list=True)
        files = map(lambda u: (u, u.data['username']), users)
        return files
    
    def getChildren(self, parent):
        return [[], self.getAll()]
