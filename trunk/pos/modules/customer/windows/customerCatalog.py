import pos

from pos.modules.customer.objects.customer import Customer
from pos.modules.customer.objects.group import CustomerGroup

from pos.modules.base.windows import Catalog

class CustomerCatalog(Catalog):
    def getAll(self, search=None):
        session = pos.database.session()
        query = session.query(Customer, Customer.name)
        if search is not None:
            query = query.filter(Customer.name.like('%%%s%%'  % (search,)))
        return query.all()

    def getChildren(self, parent):
        session = pos.database.session()
        
        if parent is None:
            return [session.query(CustomerGroup, CustomerGroup.name).all(),
                    session.query(Customer, Customer.name).filter(~Customer.groups.any()).all()]
        else:
            return [[],
                    session.query(Customer, Customer.name).filter(Customer.groups.contains(parent)).all()]

        return [[(c, c.name) for c in children_customers]]
