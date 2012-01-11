import pos
from pos.modules import Module

class ModuleLoader(Module):
    dependencies = ('base', 'currency')
    config = []
    name = 'Customer and Customer Groups Support'

    def load(self):
        from pos.modules.customer.objects.customer import Customer
        from pos.modules.customer.objects.group import CustomerGroup
        from pos.modules.customer.objects.contact import CustomerContact
        from pos.modules.customer.objects.address import CustomerAddress
        return [Customer, CustomerGroup, CustomerContact, CustomerAddress]

    def test(self):
        from pos.modules.customer.objects.customer import Customer
        from pos.modules.customer.objects.group import CustomerGroup
        from pos.modules.customer.objects.contact import CustomerContact
        from pos.modules.customer.objects.address import CustomerAddress
    
        session = pos.database.session()
    
        cg1 = CustomerGroup(name='Delivery', comment='Customers whose newspapers are being delivered to.')
        cg2 = CustomerGroup(name='Library', comment='Customers who have an account at the library.')
        cg3 = CustomerGroup(name='Offices', comment='Customers who buy products for their offices and/or companies.')
        
        from pos.modules.currency.objects.currency import Currency
        LL = session.query(Currency).filter_by(id=1).one()
        
        c1 = Customer(name='Abou El Jouj', code=None, first_name='Jad', last_name='Kik',
                      max_debt=200000, currency=LL, comment='This guy talks too much.', discount=0.5, groups=[cg1, cg2])
        c2 = Customer(name='Abou El Imm', code='123', first_name='Imad', last_name='Ferneine',
                      max_debt=None, currency=LL, comment='He is egyptian!', discount=0, groups=[cg3])
    
        cc1 = CustomerContact(name='email', value='jadkik94@gmail.com', customer=c1)
        cc2 = CustomerContact(name='mobile', value='70695924', customer=c1)
        cc3 = CustomerContact(name='phone', value='04972721', customer=c1)
        cc4 = CustomerContact(name='phone', value='+9701238422', customer=c2)
        
        ca1 = CustomerAddress(country='Lebanon', region='Metn', city='Beit Mery', details='Tal3it Kafra', customer=c1)
        ca2 = CustomerAddress(country='Lebanon', region='Beirut', city='Ashrafieh', details='7ad el dekkeneh', customer=c2)
    
        session.add(c1)
        session.add(c2)
        session.commit()

    def menu(self):
        from pos.modules.customer.panels import CustomersPanel
        from pos.modules.customer.panels import CustomerGroupsPanel
            
        return [[{'label': 'Customers', 'rel': 1, 'priority': 3}],
                [{'parent': 'Customers', 'label': 'Customers', 'page': CustomersPanel},
                 {'parent': 'Customers', 'label': 'Groups', 'page': CustomerGroupsPanel},]]
