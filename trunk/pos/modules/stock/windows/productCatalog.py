import pos

from pos.modules.stock.objects.category import Category
from pos.modules.stock.objects.product import Product

from pos.modules.base.windows import Catalog

class ProductCatalog(Catalog):
    def __init__(self, parent,
                 show_all_item=True, show_search_box=True, show_only_in_stock=False):
        self.show_only_in_stock = show_only_in_stock
        Catalog.__init__(self, parent,
                         show_all_item=show_all_item, show_search_box=show_search_box)
    
    def getAll(self, search=None):
        session = pos.database.session()
        query = session.query(Product, Product.name)
        if self.show_only_in_stock:
            query = query.filter(Product.in_stock)
        if search is not None:
            query = query.filter(Product.name.like('%%%s%%' % (search,)))
        return query.all()
    
    def getChildren(self, parent):
        session = pos.database.session()
        product_query = session.query(Product, Product.name)
        if self.show_only_in_stock:
            product_query = product_query.filter(Product.in_stock)
        return [session.query(Category, Category.name).filter(Category.parent == parent).all(),
                product_query.filter(Product.category == parent).all()]
