import pos
from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

dependencies = ('base',)

def configDB(test=False):
    pos.db.query("""CREATE TABLE categories (
         id int AUTO_INCREMENT PRIMARY KEY,
         name varchar(255) NOT NULL,
         parent_id int DEFAULT NULL,
         state int NOT NULL DEFAULT 1,
         FOREIGN KEY (parent_id) REFERENCES categories(id)
    )""")

    pos.db.query("""CREATE TABLE products (
         id int AUTO_INCREMENT PRIMARY KEY,
         name varchar(255) NOT NULL,
         description varchar(255) NOT NULL DEFAULT '',
         reference varchar(255) NOT NULL DEFAULT '',
         code varchar(255) NOT NULL DEFAULT '',
         price double NOT NULL DEFAULT 0,
         currency_id int NOT NULL DEFAULT 1,
         quantity int DEFAULT NULL,
         category_id int DEFAULT NULL,
         state int NOT NULL DEFAULT 1,
         FOREIGN KEY (currency_id) REFERENCES currencies(id),
         FOREIGN KEY (category_id) REFERENCES categories(id)
    )""")

    pos.db.query("""CREATE TABLE stockdiary (
         id int AUTO_INCREMENT PRIMARY KEY,
         operation enum('in', 'out', 'edit') NOT NULL,
         quantity INT NOT NULL,
         date DATETIME NOT NULL,
         product_id INT NOT NULL,
         FOREIGN KEY (product_id) REFERENCES products(id)
    )""")

    if not test: return

    pos.db.query("""INSERT INTO categories (name, parent_id) VALUES
        ('Root', NULL),
        ('Sub1', 1),
        ('Sub2', 1),
        ('Sub2-Sub1', 3),
        ('Root2', NULL)
    """)

    pos.db.query("""INSERT INTO products (name, description, reference, code, price, currency_id, quantity, category_id) VALUES
        ('CRAYONS 12pc. MAPED', 'Boite de 12 crayons Maped', '123', '000987654', 1500, 1, 10, 2),
        ('GOMME RONDE MAPED', 'Gomme ronde de Maped avec couvercle', 'G32', '11998877', 3000, 1, 5, 2),
        ('PHOTOCOPIE N/B', 'Photocopie en noir et blanc', '', 'DY6', 500, 1, NULL, 1),
        ('JOURNAL AN NAHAR', 'Quotidien libanais an-nahar', '', 'jrnal123', 2, 2, NULL, 5)
    """)

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu
        MenuRoot(self.menu, "Stock", 'stock')

    def loadSubItems(self):
        from pos.modules.stock.panels import CategoriesPanel
        from pos.modules.stock.panels import ProductsPanel
        from pos.modules.stock.panels import StockDiaryPanel
        
        MenuItem(self.menu, "Stock", "Products", ProductsPanel)
        MenuItem(self.menu, "Stock", "Categories", CategoriesPanel)
        MenuItem(self.menu, "Stock", "Stock Diary", StockDiaryPanel)
