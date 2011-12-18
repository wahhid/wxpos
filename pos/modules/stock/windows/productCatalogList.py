import pos

from pos.modules.stock.objects.category import Category
from pos.modules.stock.objects.product import Product

from pos.modules.base.windows.catalogList import CatalogList

class ProductCatalogList(CatalogList):
    def __init__(self, parent, show_only_in_stock=False):
        CatalogList.__init__(self, parent)
        self.show_only_in_stock = show_only_in_stock
    
    def getAll(self):
        session = pos.database.session()
        if self.show_only_in_stock:
            return session.query(Product, Product.name).filter(Product.in_stock).all()
        else:
            return session.query(Product, Product.name).all()
    
    def getChildren(self, parent):
        session = pos.database.session()
        return [session.query(Category, Category.name).filter(Category.parent == parent).all(),
                session.query(Product, Product.name).filter(Product.category == parent).all()]
