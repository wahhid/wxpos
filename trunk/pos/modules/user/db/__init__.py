from .user import UserDB
from .role import RoleDB
from .permission import PermissionDB

from pos.db.subset import DBSubset

class ModuleDB(DBSubset, UserDB, RoleDB, PermissionDB):
    pass

def config(db):
    db.createTable("roles", """
         id int AUTO_INCREMENT PRIMARY KEY,
         name varchar(255) NOT NULL UNIQUE
    """)

    db.createTable("permissions", """
         id int AUTO_INCREMENT PRIMARY KEY,
         name varchar(255) NOT NULL UNIQUE,
         description varchar(255)
    """)

    db.createTable("role_permission", """
         role_id int NOT NULL,
         permission_id int NOT NULL,
         PRIMARY KEY (role_id, permission_id),
         FOREIGN KEY (role_id) REFERENCES roles(id),
         FOREIGN KEY (permission_id) REFERENCES permissions(id)
    """)

    db.createTable("users", """
         id int AUTO_INCREMENT PRIMARY KEY,
         username varchar(255) NOT NULL UNIQUE,
         password varchar(32) NOT NULL,
         role_id int NOT NULL,
         state int NOT NULL DEFAULT 1,
         FOREIGN KEY (role_id) REFERENCES roles(id)
    """)

    db.query("modules.user.db.config", """INSERT INTO roles (name) VALUES
        ('admin'), ('manager'), ('employee')
    """)

    db.query("modules.user.db.config", """INSERT INTO permissions (name, description) VALUES
        ('users', 'Manage users, permissions and roles.'),
        ('sales', 'Manage sales: tickets and orders.'),
        ('cash', 'Manage cash register: close cash and manage payments.'),
        ('stock', 'Manage products and categories in stock.'),
        ('customers', 'Manage customers.'),
        ('reports', 'View and print reports.'),
        ('system', 'Edit system settings.')
    """)

    db.query("modules.user.db.config", """INSERT INTO role_permission (role_id, permission_id) VALUES
        (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
        (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
        (3, 2)
    """)

    db.query("modules.user.db.config", """INSERT INTO users (username, password, role_id, state) VALUES
        ('Admin', MD5('admin'), 1, 1),
        ('Manager', MD5('manager'), 2, 1),
        ('Employee', MD5('employee'), 3, 1)
    """)
