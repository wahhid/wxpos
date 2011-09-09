import pos
from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

dependencies = ('base', 'currency', 'user', 'stock', 'customer')

def configDB(test=False):
    pos.db.query("""CREATE TABLE tickets (
         id int AUTO_INCREMENT PRIMARY KEY,
         comment varchar(255) DEFAULT NULL,
         date_open DATETIME DEFAULT NULL,
         date_close DATETIME DEFAULT NULL,
         payment_method int DEFAULT NULL,
         date_paid DATETIME DEFAULT NULL,
         currency_id int DEFAULT NULL,
         customer_id int DEFAULT NULL,
         user_id int NOT NULL,
         state int NOT NULL DEFAULT 1,
         FOREIGN KEY (currency_id) REFERENCES currencies(id),
         FOREIGN KEY (customer_id) REFERENCES customers(id),
         FOREIGN KEY (user_id) REFERENCES users(id)
    )""")
    
    pos.db.query("""CREATE TABLE ticketlines (
         id int AUTO_INCREMENT PRIMARY KEY,
         description varchar(255) NOT NULL,
         sell_price double NOT NULL,
         amount int NOT NULL DEFAULT 1,
         ticket_id  int NOT NULL,
         product_id int DEFAULT NULL,
         is_edited bool DEFAULT 0,
         FOREIGN KEY (ticket_id) REFERENCES tickets(id)
    )""")

    pos.db.query("""CREATE TABLE payment_methods (
         id int AUTO_INCREMENT PRIMARY KEY,
         name varchar(255) NOT NULL
    )""")

    if not test: return

    pos.db.query("""INSERT INTO payment_methods (name) VALUES
        ('cash'), ('cheque'), ('voucher'), ('card'), ('free'), ('debt')
    """)

    pos.db.query("""INSERT INTO tickets (comment, date_open, currency_id, customer_id, user_id) VALUES
        ('Test Ticket 1', NOW(), 1, NULL, 1),
        ('Test Ticket 2', NOW(), 2, 1, 1)
    """)

    pos.db.query("""INSERT INTO ticketlines (description, sell_price, amount, ticket_id, product_id, is_edited) VALUES
        ('Ticketline 1-1', 2000, 1, 1, NULL, 0),
        ('Ticketline 1-2', 4500, 3, 1, NULL, 0),
        ('Ticketline 1-3 edited from p1', 5000, 2, 1, 1, 1),
        ('Ticketline 2-1', 5, 12, 2, NULL, 0),
        ('Ticketline 2-2 ewWeErRtTyYuUiIoOpP', 1.5, 12, 2, 2, 1)
    """)

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu

    def loadSubItems(self):
        from pos.modules.sales.panels import SalesPanel
        
        MenuItem(self.menu, "Main", "Sales", SalesPanel, 'sales')
        #MenuItem(self.menu, "Main", "Orders", EmptyPanel, 'sales')
