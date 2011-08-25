from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu

    def loadSubItems(self):
        from pos.modules.sales.panels import SalesPanel
        
        MenuItem(self.menu, "Main", "Sales", SalesPanel, 'sales')
        #MenuItem(self.menu, "Main", "Orders", EmptyPanel, 'sales')

dependencies = ('base', 'user', 'stock', 'customer')
