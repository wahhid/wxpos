import pos
import os, sys
import pkgutil, importlib

class ModuleWrapper:
    """
    Wrapper around the actual installed module.
    Provides functions to make common tasks easier.
    """
    def __init__(self, pkg, parent):
        self.name = pkg[1]
        self.dependencies = []

    def load(self):
        """
        This will load the two main python modules:
        - the main module which contains the init function
        - the 'config' module which contains details for the configuration and loading of the module 
        """
        self.top_module = importlib.import_module('pos.modules.'+self.name)
        self.config_module = importlib.import_module('.config', 'pos.modules.'+self.name)
        self.dependencies = self.config_module.dependencies
        return self.top_module is not None and self.config_module is not None

    def load_database_objects(self):
        """
        Load this module's database objects for them to be usable in SQLAlchemy.
        """
        try:
            load = self.config_module.load_database_objects
        except AttributeError:
            return False
        else:
            load()
            return True

    def init(self):
        """
        Calls the init function of this module.
        Returns True if the app can continue loading, False if not, None if no init function is present.
        """
        try:
            init = self.top_module.init
        except AttributeError:
            return
        else:
            return init()

    def __lt__(self, mod):
        """
        Implements the '<' comparison operator.
        Used when sorting the list of modules, by dependencies.
        """
        return (self.name in mod.dependencies)
    
    def __repr__(self):
        return '<ModuleWrapper %s>' % (self.name, )

modules = []
def init():
    """
    Load all the modules installed (main and config).
    """
    global modules
    print '*Loading modules...'
    modules_path = os.path.dirname(__file__)
    packages = [p for p in pkgutil.walk_packages([modules_path]) if not p[1].startswith('_') and p[2]]

    modules = []
    for pkg in packages:
        mod = ModuleWrapper(pkg, modules_path)
        if not mod.load():
            if mod.top_module is None:
                print '*Invalid module', mod.name
            else:
                print '*No config module for', mod.name
        else:
            modules.append(mod)
    print '*(%d) modules found: %s' % (len(modules), ', '.join([m.name for m in modules]))
    checkDependencies()
    modules.sort()

def checkDependencies():
    """
    Check that all the installed modules' dependencies are installed.
    Else raise an exception to prevent the application from running.
    """
    print '*Checking module dependencies...'
    module_names = [mod.name for mod in modules]
    for mod in modules:
        missing = [mod_name for mod_name in mod.dependencies if mod_name not in module_names]
        if len(missing)>0:
            print '*** Missing dependencies for module', mod.name, ':', ', '.join(missing)
            raise Exception, 'Missing dependency'

def isInstalled(module_name):
    """
    Returns True if the module called module_name is installed.
    """
    return (module_name in (mod.name for mod in modules))

def all():
    """
    Returns a tuple of all the ModuleWrapper objects that are linked to all the actual modules installed.
    """
    return tuple(modules)

# DATABASE EXTENSION

def loadDB():
    """
    Load all the database objects of every module so that they can be used with SQLAlchemy.
    """
    for mod in modules:
        print '*Loading DB Objects', mod.name
        if not mod.load_database_objects():
            print '*DB Objects missing'

def configDB():
    """
    Clear and recreate the whole database.
    Note: Only the tables are changed, the database itself cannot be created or dropped.
    """
    print '*Clearing database...'
    pos.database.config.clear()
    print '*Re-creating database'
    pos.database.config.create()

def configTestDB():
    """
    Insert the test database values of every module installed.
    """
    print '*Adding test values to database...'
    for mod in modules:
        try:
            test = mod.config_module.test_database_values
        except AttributeError:
            print '*DB Test Config missing', mod.name
        else:
            print '*Adding Test Values', mod.name
            test()

# MENU EXTENSION

def extendMenu(menu):
    """
    Load all menu extensions of every module, meaning all the root items and sub-items defined.
    """
    items = []
    for mod in modules:
        try:
            item = mod.config_module.ModuleMenu
        except AttributeError:
            print '*Menu Extension missing', mod.name
        else:
            items.append(item(menu))

    for item in items:
        item.loadSubItems()
