import pos
from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

dependencies = ('base',)

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        self.menu = menu
        MenuRoot(self.menu, "Users", 'users')

    def loadSubItems(self):
        from pos.modules.user.panels import UsersPanel
        from pos.modules.user.panels import RolesPanel
        from pos.modules.user.panels import PermissionsPanel

        from pos.modules.user.panels import IndividualUserPanel
        
        MenuItem(self.menu, "Users", "Users", UsersPanel)
        MenuItem(self.menu, "Users", "Roles", RolesPanel)
        MenuItem(self.menu, "Users", "Permissions", PermissionsPanel)

        MenuItem(self.menu, "Administration", "User", IndividualUserPanel)

def configDB(test=False):
    pos.db.query("""CREATE TABLE roles (
         id int AUTO_INCREMENT PRIMARY KEY,
         name varchar(255) NOT NULL UNIQUE
    )""")

    pos.db.query("""CREATE TABLE permissions (
         id int AUTO_INCREMENT PRIMARY KEY,
         name varchar(255) NOT NULL UNIQUE,
         description varchar(255)
    )""")

    pos.db.query("""CREATE TABLE role_permission (
         role_id int NOT NULL,
         permission_id int NOT NULL,
         PRIMARY KEY (role_id, permission_id),
         FOREIGN KEY (role_id) REFERENCES roles(id),
         FOREIGN KEY (permission_id) REFERENCES permissions(id)
    )""")

    pos.db.query("""CREATE TABLE users (
         id int AUTO_INCREMENT PRIMARY KEY,
         username varchar(255) NOT NULL UNIQUE,
         password varchar(32) NOT NULL,
         role_id int NOT NULL,
         state int NOT NULL DEFAULT 1,
         FOREIGN KEY (role_id) REFERENCES roles(id)
    )""")

    if not test: return

    pos.db.query("""INSERT INTO roles (name) VALUES
        ('admin'), ('manager'), ('employee')
    """)

    pos.db.query("""INSERT INTO permissions (name, description) VALUES
        ('users', 'Manage users, permissions and roles.'),
        ('sales', 'Manage sales: tickets and orders.'),
        ('cash', 'Manage cash register: close cash and manage payments.'),
        ('stock', 'Manage products and categories in stock.'),
        ('customers', 'Manage customers.'),
        ('reports', 'View and print reports.'),
        ('system', 'Edit system settings.')
    """)

    pos.db.query("""INSERT INTO role_permission (role_id, permission_id) VALUES
        (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
        (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
        (3, 2)
    """)

    pos.db.query("""INSERT INTO users (username, password, role_id, state) VALUES
        ('Admin', MD5('admin'), 1, 1),
        ('Manager', MD5('manager'), 2, 1),
        ('Employee', MD5('employee'), 3, 1)
    """)
