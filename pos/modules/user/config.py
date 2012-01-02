import pos
from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

dependencies = ('base',)

pos.config.set_default('mod.user', 'allow_empty_passwords', '1')

def load_database_objects():
    from pos.modules.user.objects.permission import Permission, MenuRestriction
    from pos.modules.user.objects.role import Role
    from pos.modules.user.objects.user import User

def test_database_values():
    from pos.modules.user.objects.permission import Permission, MenuRestriction
    from pos.modules.user.objects.role import Role
    from pos.modules.user.objects.user import User

    mr = lambda root, item: MenuRestriction(root=root, item=item)

    permissions_text = [
        ('common', 'Manage own user information', [mr('Administration', 'User')]),
        ('users', 'Manage users, permissions and roles.', [mr('Users', 'Users'), mr('Users', 'Roles'), mr('Users', 'Permissions')]),
        ('sales', 'Manage sales: tickets and orders.', [mr('Main', 'Sales'), mr('Main', 'Debts')]),
        ('cash', 'Manage cash register: close cash and manage payments.', []),
        ('stock', 'Manage products and categories in stock.', [mr('Stock', 'Products'), mr('Stock', 'Categories'), mr('Stock', 'Stock Diary')]),
        ('customers', 'Manage customers.', [mr('Customers', 'Customers'), mr('Customers', 'Groups')]),
        ('reports', 'View and print reports.', [mr('Reports', 'Sales'), mr('Reports', 'Customers'), mr('Reports', 'Stock'), mr('Reports', 'Stock Diary'), mr('Reports', 'Users')]),
        ('system', 'Edit system settings.', [mr('System', 'Configuration'), mr('System', 'Currencies')])]
    permissions = [Permission(name=p[0], description=p[1], menu_restrictions=p[2]) for p in permissions_text]

    admin_permissions = map(lambda p: permissions[p], range(len(permissions)))
    manager_permissions = map(lambda p: permissions[p], [0, 2, 3, 4, 5, 6])
    employee_permissions = map(lambda p: permissions[p], [0, 2])

    admin_role = Role(name='admin', permissions=admin_permissions)
    manager_role = Role(name='manager', permissions=manager_permissions)
    employee_role = Role(name='employee', permissions=employee_permissions)

    admin_user = User(username='Admin', password='admin', role=admin_role)
    manager_user = User(username='Manager', password='manager', role=manager_role)
    employee_user = User(username='Employee', password='employee', role=employee_role)

    session = pos.database.session()
    session.add(admin_user)
    session.add(manager_user)
    session.add(employee_user)
    session.commit()

class ModuleMenu(ModuleMenuBase):
    def __init__(self, menu):
        ModuleMenuBase.__init__(self, menu)
        MenuRoot(self.menu, "Users", rel=-2, priority=3)

    def loadSubItems(self):
        from pos.modules.user.panels import UsersPanel
        from pos.modules.user.panels import RolesPanel
        from pos.modules.user.panels import PermissionsPanel

        from pos.modules.user.panels import IndividualUserPanel
        
        MenuItem(self.menu, "Users", "Users", UsersPanel)
        MenuItem(self.menu, "Users", "Roles", RolesPanel)
        MenuItem(self.menu, "Users", "Permissions", PermissionsPanel)

        MenuItem(self.menu, "Administration", "User", IndividualUserPanel)
