import pos
from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

dependencies = ('base', 'currency')

def load_database_objects():
    from pos.modules.stock.objects.category import Category
    from pos.modules.stock.objects.product import Product

def test_database_values():
    from pos.modules.stock.objects.category import Category
    from pos.modules.stock.objects.product import Product

    session = pos.database.session()

    cat1 = Category('Root1', None)
    cat2 = Category('Sub1', cat1)
    cat3 = Category('Sub2', cat1)
    cat4 = Category('Sub2-Sub1', cat3)
    cat5 = Category('Root2', None)

    from pos.modules.currency.objects.currency import Currency
    LL = session.query(Currency).filter_by(id=1).one()
    EUR = session.query(Currency).filter_by(id=3).one()

    p1 = Product('MAPED PENCILS 12-BOX', '12 pencils box Maped', 'ref123', 'code123', 1000, LL, 10, cat1)
    p2 = Product('MAPED SINGLE PENCIL', '1 pencil Maped', 'ref122', 'code12345', 250, LL, 20, cat2)
    p3 = Product('MAPED ERASER', 'Rounded Maped Eraser', 'ref133', 'code456', 2, EUR, 5, cat3)
    p4 = Product('PHOTOCOPY B/W', 'Black and White Photocopy', '', '12345', 250, LL, None, cat4, False)
    p5 = Product('ANNAHAR', 'An-Nahar Lebanese Daily Newspaper', '789', 'barcode135', 2000, LL, None, cat5, False)

    [session.add(p) for p in (p1, p2, p3, p4, p5)]
    session.commit()

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        ModuleMenuBase.__init__(self, menu)
        MenuRoot(self.menu, "Stock") #perm:stock

    def loadSubItems(self):
        from pos.modules.stock.panels import CategoriesPanel
        from pos.modules.stock.panels import ProductsPanel
        from pos.modules.stock.panels import StockDiaryPanel
        
        MenuItem(self.menu, "Stock", "Products", ProductsPanel)
        MenuItem(self.menu, "Stock", "Categories", CategoriesPanel)
        MenuItem(self.menu, "Stock", "Stock Diary", StockDiaryPanel)
