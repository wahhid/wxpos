import pos.modules.stock.objects.category as category
import pos.modules.stock.objects.product as product

from pos.modules.base.windows.catalogList import CatalogList

class ProductCatalogList(CatalogList):
    def __init__(self, parent, show_only_in_stock=False):
        CatalogList.__init__(self, parent)
        self.show_only_in_stock = show_only_in_stock
    
    def getAll(self):
        if self.show_only_in_stock:
            products = product.find(list=True, in_stock=True)
        else:
            products = product.find(list=True)
        files = map(lambda p: (p, p.data['name']), products)
        return files
    
    def getChildren(self, parent):
        children_categories = category.find(list=True, parent_category=parent)
        children_products = product.find(list=True, category=parent)

        return [map(lambda c: (c, c.data['name']), children_categories),
                map(lambda p: (p, p.data['name']), children_products)]
