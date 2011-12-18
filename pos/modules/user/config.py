import pos
from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

dependencies = ('base',)

def load_database_objects():
    from pos.modules.user.objects.permission import Permission
    from pos.modules.user.objects.role import Role
    from pos.modules.user.objects.user import User

def test_database_values():
    from pos.modules.user.objects.permission import Permission
    from pos.modules.user.objects.role import Role
    from pos.modules.user.objects.user import User

    permissions_text = [('users', 'Manage users, permissions and roles.'),
        ('sales', 'Manage sales: tickets and orders.'),
        ('cash', 'Manage cash register: close cash and manage payments.'),
        ('stock', 'Manage products and categories in stock.'),
        ('customers', 'Manage customers.'),
        ('reports', 'View and print reports.'),
        ('system', 'Edit system settings.')]
    permissions = map(lambda p: Permission(p[0], p[1]), permissions_text)

    admin_permissions = map(lambda p: permissions[p], [0, 1, 2, 3, 4, 5, 6])
    manager_permissions = map(lambda p: permissions[p], [1, 2, 3, 4, 5])
    employee_permissions = map(lambda p: permissions[p], [1])

    admin_role = Role('admin', admin_permissions)
    manager_role = Role('manager', manager_permissions)
    employee_role = Role('employee', employee_permissions)

    admin_user = User('Admin', 'admin', admin_role)
    manager_user = User('Manager', 'manager', manager_role)
    employee_user = User('Employee', 'employee', employee_role)

    session = pos.database.session()
    session.add(admin_user)
    session.add(manager_user)
    session.add(employee_user)
    session.commit()

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
