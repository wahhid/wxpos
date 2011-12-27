import pos
import os, sys
import pkgutil, importlib

class ModuleWrapper:
    def __init__(self, pkg, parent):
        self.name = pkg[1]
        self.dependencies = []

    def load(self):
        self.top_module = importlib.import_module('pos.modules.'+self.name)
        self.config_module = importlib.import_module('.config', 'pos.modules.'+self.name)
        self.dependencies = self.config_module.dependencies
        return self.top_module is not None and self.config_module is not None

    def load_database_objects(self):
        try:
            load = self.config_module.load_database_objects
        except AttributeError:
            return False
        else:
            load()
            return True

    def init(self):
        try:
            init = self.top_module.init
        except AttributeError:
            return
        else:
            return init()

    def __lt__(self, mod):
        return (self.name in mod.dependencies)
    
    def __repr__(self):
        return '<ModuleWrapper %s>' % (self.name, )

modules = []
def init():
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
    print '*Checking module dependencies...'
    module_names = [mod.name for mod in modules]
    for mod in modules:
        missing = [mod_name for mod_name in mod.dependencies if mod_name not in module_names]
        if len(missing)>0:
            print '*** Missing dependencies for module', mod.name, ':', ', '.join(missing)
            raise Exception, 'Missing dependency'

def isInstalled(module_name):
    return (module_name in (mod.name for mod in modules))

def all():
    return tuple(modules)

# DATABASE EXTENSION

def loadDB():
    for mod in modules:
        print '*Loading DB Objects', mod.name
        if not mod.load_database_objects():
            print '*DB Objects missing'

def configDB():
    print '*Clearing database...'
    pos.database.config.clear()
    print '*Re-creating database'
    pos.database.config.create()

def configTestDB():
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
