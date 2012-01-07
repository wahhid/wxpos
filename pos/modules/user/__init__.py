
def init():
    import wx
    import pos
    from .dialogs import LoginDialog
    import pos.modules.user.objects.user as user
    from pos.modules.user.objects.user import User
    from pos.modules.user.objects.superuser import SuperUser
    
    session = pos.database.session()
    user_count = session.query(User).count()
    if user_count > 0:
        login = LoginDialog(None)
        result = login.ShowModal()
        if user.current is None:
            return False
        else:
            # Filter menu items to display according to permissions
            restrictions = [(mr.root, mr.item) for mr in user.current.menu_restrictions] 
            for item in pos.menu.main.getItems():
                item.children = [i for i in item.children if (item.label, i.label) in restrictions]
            return True
    else:
        user.current = SuperUser()
        wx.MessageBox('No user found. Using Super User.\nCreate a user as soon as possible.\nUse F3 to login as superuser again.', 'Login', style=wx.ICON_INFORMATION | wx.OK)
        return True
