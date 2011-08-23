import wx
from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu
        MenuRoot(self.menu, "Main")
        MenuRoot(self.menu, "Administration")
        MenuRoot(self.menu, "System", 'system')

    def loadSubItems(self):
        MenuItem(self.menu, "System", "Configuration", wx.Panel, 'system')

dependencies = tuple()
