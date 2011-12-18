import pos
from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey

dependencies = ('base', 'currency')

def load_database_objects():
    from pos.modules.customer.objects.customer import Customer
    from pos.modules.customer.objects.customergroup import CustomerGroup

def test_database_values():
    from pos.modules.customer.objects.customer import Customer
    from pos.modules.customer.objects.customergroup import CustomerGroup

    session = pos.database.session()

    cg1 = CustomerGroup('Delivery', 'Customers whose newspapers are being delivered to.')
    cg2 = CustomerGroup('Library', 'Customers who have an account at the library.')
    cg3 = CustomerGroup('Offices', 'Customers who buy products for their offices and/or companies.')
    
    from pos.modules.currency.objects.currency import Currency
    LL = session.query(Currency).filter_by(id=1).one()
    
    c1 = Customer('Abou El Jouj', None, 'Jad', 'Kik', 200000, LL, 'This guy talks too much.', [cg1, cg2])
    c2 = Customer('Abou El Imm', '123', 'Imad', 'Ferneine', None, LL, 'He is egyptian!', [cg3])

    session.add(c1)
    session.add(c2)
    session.commit()

def configDB(test=False):
    pos.db.query("""CREATE TABLE contact (
         id int AUTO_INCREMENT PRIMARY KEY,
         name enum('email', 'phone', 'number') NOT NULL,
         value varchar(255) NOT NULL,
         customer_id int NOT NULL
    )""")

    pos.db.query("""CREATE TABLE address (
         id int AUTO_INCREMENT PRIMARY KEY,
         country varchar(255),
         region varchar(255),
         city varchar(255),
         details varchar(255),
         customer_id int NOT NULL
    )""")

    pos.db.query("""INSERT INTO contact (name, value, customer_id) VALUES
        ('email', 'jadkik94@gmail.com', 1),
        ('phone', '70695924', 1),
        ('phone', '04972721', 1),
        ('phone', '+9701238422', 2)
    """)

    pos.db.query("""INSERT INTO address (country, region, city, details, customer_id) VALUES
        ('Lebanon', 'Metn', 'Beit Mery', 'tal3it kafra', 1),
        ('Lebanon', 'Beirut', 'Ashrafieh', '7ad el dekkeneh', 2)
    """)

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu
        MenuRoot(self.menu, "Customers", 'customers')

    def loadSubItems(self):
        from pos.modules.customer.panels import CustomersPanel
        from pos.modules.customer.panels import CustomerGroupsPanel
        
        MenuItem(self.menu, "Customers", "Customers", CustomersPanel)
        MenuItem(self.menu, "Customers", "Groups", CustomerGroupsPanel)
