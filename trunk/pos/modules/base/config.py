from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

dependencies = tuple()

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        ModuleMenuBase.__init__(self, menu)
        MenuRoot(self.menu, "Main", rel=0, priority=5)
        MenuRoot(self.menu, "System", rel=-1, priority=4)#perm:system
        MenuRoot(self.menu, "Administration", rel=-1, priority=5)

    def loadSubItems(self):
        from pos.modules.base.panels import MainConfigPanel
        
        MenuItem(self.menu, "System", "Configuration", MainConfigPanel)
