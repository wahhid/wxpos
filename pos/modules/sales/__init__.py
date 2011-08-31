import pos
from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

dependencies = ('base', 'user', 'stock', 'customer')

def configDB(test=False):
    pos.db.query("""CREATE TABLE tickets (
         id int AUTO_INCREMENT PRIMARY KEY,
         comment varchar(255) DEFAULT NULL,
         date_open DATETIME DEFAULT NULL,
         date_close DATETIME DEFAULT NULL,
         customer_id int DEFAULT NULL,
         user_id int NOT NULL,
         state int NOT NULL DEFAULT 1,
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

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu

    def loadSubItems(self):
        from pos.modules.sales.panels import SalesPanel
        
        MenuItem(self.menu, "Main", "Sales", SalesPanel, 'sales')
        #MenuItem(self.menu, "Main", "Orders", EmptyPanel, 'sales')
