import pos
from pos.modules import Module

class ModuleLoader(Module):
    dependencies = ('base',)
    config = [['mod.user', {'allow_empty_passwords': '1'}]]
    name = 'Users, Permissions and Authentication Support'

    def load(self):
        from pos.modules.user.objects.permission import Permission, MenuRestriction
        from pos.modules.user.objects.role import Role
        from pos.modules.user.objects.user import User
        return [Permission, MenuRestriction, Role, User]

    def test(self):
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

    def menu(self):
        from pos.modules.user.panels import UsersPanel
        from pos.modules.user.panels import RolesPanel
        from pos.modules.user.panels import PermissionsPanel
        
        from pos.modules.user.panels import IndividualUserPanel
        
        return [[{'label': 'Users', 'rel': -2, 'priority': 3}],
                [{'parent': 'Users', 'label': 'Users', 'page': UsersPanel},
                 {'parent': 'Users', 'label': 'Roles', 'page': RolesPanel},
                 {'parent': 'Users', 'label': 'Permissions', 'page': PermissionsPanel},
                 {'parent': 'Administration', 'label': 'User', 'page': IndividualUserPanel}]]

    def init(self):
        import wx
        from .dialogs import LoginDialog
        import pos.modules.user.objects.user as user
        from pos.modules.user.objects.user import User
        from pos.modules.user.objects.superuser import SuperUser
        
        session = pos.database.session()
        user_count = session.query(User).count()
        if user_count > 0:
            login = LoginDialog(None)
            result = login.ShowModal()
            if user.current is None:
                return False
            elif isinstance(user.current, SuperUser):
                return True
            else:
                # Filter menu items to display according to permissions
                restrictions = [(mr.root, mr.item) for mr in user.current.menu_restrictions] 
                for root in pos.menu.main.getItems():
                    for item in root.children:
                        item.enabled = ((root.label, item.label) in restrictions)
                return True
        else:
            user.current = SuperUser()
            wx.MessageBox('No user found. Using Super User.\nCreate a user as soon as possible.\nUse F3 to login as superuser again.', 'Login', style=wx.ICON_INFORMATION | wx.OK)
            return True
