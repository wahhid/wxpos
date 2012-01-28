import wx

import pos

from pos.modules.user.objects.user import User

from pos.modules.base.windows import Catalog

class UserCatalog(Catalog):
    def __init__(self, parent,
                 show_all_item=True, show_search_box=True, show_hidden=False):
        self.show_hidden = show_hidden
        Catalog.__init__(self, parent,
                             file_bmp=wx.Bitmap('./res/user/images/user.png', wx.BITMAP_TYPE_PNG),
                             show_all_item=show_all_item, show_search_box=show_search_box)
    
    def getAll(self, search=None):
        session = pos.database.session()
        query = session.query(User, User.username)
        if not self.show_hidden:
            query = query.filter_by(hidden=False)
        if search is not None:
            query = query.filter(User.username.like('%%%s%%' % (search,)))
        return query.all()
    
    def getChildren(self, parent):
        return [[], self.getAll()]
