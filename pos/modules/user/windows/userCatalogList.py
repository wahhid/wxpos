import wx

import pos

from pos.modules.user.objects.user import User

from pos.modules.base.windows.catalogList import CatalogList

class UserCatalogList(CatalogList):
    def __init__(self, parent, show_hidden=False):
        self.show_hidden = show_hidden
        CatalogList.__init__(self, parent,
                             file_bmp=wx.Bitmap('images/user.png', wx.BITMAP_TYPE_PNG),
                             show_all_item=False)
    
    def getAll(self):
        session = pos.database.session()
        query = session.query(User, User.username)
        if not self.show_hidden:
            query = query.filter_by(hidden=False)
        return query.all()
    
    def getChildren(self, parent):
        return [[], self.getAll()]
