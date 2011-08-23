from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu
        MenuRoot(self.menu, "Customers", 'customers')

    def loadSubItems(self):
        from pos.modules.customer.panels import CustomersPanel
        from pos.modules.customer.panels import CustomergroupsPanel
        
        MenuItem(self.menu, "Customers", "Customers", CustomersPanel)
        MenuItem(self.menu, "Customers", "Groups", CustomergroupsPanel)

dependencies = ('base',)
