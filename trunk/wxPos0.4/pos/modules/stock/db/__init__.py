from .category import CategoryDB
from .product import ProductDB

from pos.db.subset import DBSubset

class ModuleDB(DBSubset, CategoryDB, ProductDB):
    pass

def config(db):
    db.createTable("categories", """
         id int AUTO_INCREMENT PRIMARY KEY,
         name varchar(255) NOT NULL,
         parent_id int DEFAULT NULL,
         state int NOT NULL DEFAULT 1,
         FOREIGN KEY (parent_id) REFERENCES categories(id)
    """)

    db.createTable("products", """
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
    """)

    db.createTable("stockdiary", """
         id int AUTO_INCREMENT PRIMARY KEY,
         action enum('in', 'out', 'edit') NOT NULL,
         quantity INT NOT NULL,
         date DATETIME NOT NULL,
         product_id INT NOT NULL,
         FOREIGN KEY (product_id) REFERENCES products(id)
    """)

    db.query("modules.user.db.config", """INSERT INTO categories (name, parent_id) VALUES
        ('Root', NULL),
        ('Sub1', 1),
        ('Sub2', 1),
        ('Sub2-Sub1', 3),
        ('Root2', NULL)
    """)

    db.query("modules.user.db.config", """INSERT INTO products (name, description, reference, code, price, currency_id, quantity, category_id) VALUES
        ('CRAYONS 12pc. MAPED', 'Boite de 12 crayons Maped', '123', '000987654', 1500, 1, 10, 2),
        ('GOMME RONDE MAPED', 'Gomme ronde de Maped avec couvercle', 'G32', '11998877', 3000, 1, 5, 2),
        ('PHOTOCOPIE N/B', 'Photocopie en noir et blanc', '', 'DY6', 500, 1, NULL, 1),
        ('JOURNAL AN NAHAR', 'Quotidien libanais an-nahar', '', 'jrnal123', 2, 2, NULL, 5)
    """)
