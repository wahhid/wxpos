from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

dependencies = tuple()

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu
        MenuRoot(self.menu, "Main")
        MenuRoot(self.menu, "Administration")
        MenuRoot(self.menu, "System", 'system')

    def loadSubItems(self):
        from pos.modules.base.panels import MainConfigPanel
        
        MenuItem(self.menu, "System", "Configuration", MainConfigPanel, 'system')
