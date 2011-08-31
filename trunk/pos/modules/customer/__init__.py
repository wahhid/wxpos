import pos
from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

dependencies = ('base',)

def configDB(test=False):
    pos.db.query("""CREATE TABLE customers (
         id int AUTO_INCREMENT PRIMARY KEY,
         name varchar(255) NOT NULL,
         code varchar(255) DEFAULT NULL,
         first_name varchar(255) DEFAULT NULL,
         last_name varchar(255) DEFAULT NULL,
         max_debt double DEFAULT NULL,
         comment varchar(255) DEFAULT NULL,
         state int NOT NULL DEFAULT 1
    )""")

    pos.db.query("""CREATE TABLE customergroups (
         id int AUTO_INCREMENT PRIMARY KEY,
         name varchar(255) NOT NULL,
         comment varchar(255) DEFAULT NULL,
         state int NOT NULL DEFAULT 1
    )""")

    pos.db.query("""CREATE TABLE customer_group (
         customer_id int NOT NULL,
         group_id int NOT NULL
    )""")

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

    if not test: return

    pos.db.query("""INSERT INTO customers (name, first_name, last_name, max_debt, comment) VALUES
        ('Abou el jouj', 'Jad', 'Kik', 200000, 'This guy talks too much.'),
        ('Abou le Imm', 'Imad', 'Ferneine', NULL, 'He is egyptian!')
    """)

    pos.db.query("""INSERT INTO customergroups (name, comment) VALUES
        ('Delivery', 'Clients whose newspapers are being delivered to.'),
        ('Library', 'Clients who have an account at the library.'),
        ('Offices/Companies', 'Clients who buy products for their offices and/or companies.')
    """)

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

    pos.db.query("""INSERT INTO customer_group (customer_id, group_id) VALUES
        (1, 1), (1, 2),
        (2, 3)
    """)

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu
        MenuRoot(self.menu, "Customers", 'customers')

    def loadSubItems(self):
        from pos.modules.customer.panels import CustomersPanel
        from pos.modules.customer.panels import CustomergroupsPanel
        
        MenuItem(self.menu, "Customers", "Customers", CustomersPanel)
        MenuItem(self.menu, "Customers", "Groups", CustomergroupsPanel)
