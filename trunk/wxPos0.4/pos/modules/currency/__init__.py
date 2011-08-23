from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu

    def loadSubItems(self):
        from pos.modules.currency.panels import CurrenciesPanel
        
        MenuItem(self.menu, "System", "Currencies", CurrenciesPanel)

dependencies = ('base',)
