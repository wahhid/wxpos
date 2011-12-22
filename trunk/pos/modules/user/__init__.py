
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
        return (user.current is not None)
    else:
        user.current = SuperUser()
        wx.MessageBox('No user found. Using Super User.\nCreate a user as soon as possible.\nUse F3 to login as superuser again.', 'Login', style=wx.ICON_INFORMATION | wx.OK)
        return True