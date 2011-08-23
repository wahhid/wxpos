from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu
        MenuRoot(self.menu, "Users", 'users')

    def loadSubItems(self):
        from pos.modules.user.panels import UsersPanel
        from pos.modules.user.panels import RolesPanel
        from pos.modules.user.panels import PermissionsPanel

        from pos.modules.user.panels import IndividualUserPanel
        
        MenuItem(self.menu, "Users", "Users", UsersPanel)
        MenuItem(self.menu, "Users", "Roles", RolesPanel)
        MenuItem(self.menu, "Users", "Permissions", PermissionsPanel)

        MenuItem(self.menu, "Administration", "User", IndividualUserPanel)

dependencies = ('base',)
