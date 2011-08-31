import pos.modules.customer.objects.customer as customer
import pos.modules.customer.objects.customergroup as customergroup

from pos.modules.base.windows.catalogList import CatalogList

class CustomerCatalogList(CatalogList):
    def getAll(self):
        customers = customer.find(list=True)
        files = map(lambda c: (c, c.data['name']), customers)
        return files
        
    def getChildren(self, parent):
        children_groups = customergroup.find(list=True) if parent is None else []
        folders = map(lambda cg: (cg, cg.data['name']), children_groups)

        if parent is None:
            children_customers = customer.find(list=True, groups=[])
        else:
            customers = customer.find(list=True)
            children_customers = filter(lambda c: parent in c.data['groups'], customers)
        files = map(lambda c: (c, c.data['name']), children_customers)

        return [folders, files]
