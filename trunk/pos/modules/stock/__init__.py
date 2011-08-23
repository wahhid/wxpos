from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu
        MenuRoot(self.menu, "Stock", 'stock')

    def loadSubItems(self):
        from pos.modules.stock.panels import CategoriesPanel
        from pos.modules.stock.panels import ProductsPanel
        
        MenuItem(self.menu, "Stock", "Products", ProductsPanel)
        MenuItem(self.menu, "Stock", "Categories", CategoriesPanel)

dependencies = ('base',)
