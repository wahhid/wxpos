import pos

from pos.modules.customer.objects.customer import Customer
from pos.modules.customer.objects.customergroup import CustomerGroup

from pos.modules.base.windows.catalogList import CatalogList

class CustomerCatalogList(CatalogList):
    def getAll(self):
        session = pos.database.session()
        return session.query(Customer, Customer.name).all()

    def getChildren(self, parent):
        session = pos.database.session()
        
        if parent is None:
            return [session.query(CustomerGroup, CustomerGroup.name).all(),
                    session.query(Customer, Customer.name).filter(~Customer.groups.any()).all()]
        else:
            return [[],
                    session.query(Customer, Customer.name).filter(Customer.groups.contains(parent)).all()]

        return [[(c, c.name) for c in children_customers]]
