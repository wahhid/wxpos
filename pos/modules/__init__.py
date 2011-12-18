import pos
import imp, os, sys
import pkgutil

class ModuleWrapper:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.cfg = None
        self.valid = None
        self.dependencies = []

    def find(self):
        try:
            _file, pathname, description = imp.find_module(self.name, [self.parent])
        except ImportError as e:
            self.valid = False
            return None
        else:
            try:
                self.cfg = imp.find_module('config', [pathname])
            except ImportError as e:
                self.valid = False
                return False
            else:
                self.valid = True
                return True
        return self.valid

    def load(self):
        if not self.valid: return
        self.top_module = imp.load_package(self.name, self.parent)
        self.module = imp.load_module(self.name+'.config', *self.cfg)
        self.dependencies = self.module.dependencies

    def load_database_objects(self):
        if not self.valid: return
        try:
            load = self.module.load_database_objects
        except AttributeError:
            return False
        else:
            load()
            return True

    def __lt__(self, mod):
        return (self.name in mod.dependencies)

def init():
    global modules
    print '*Loading modules...'
    modules_path = os.path.dirname(__file__)
    packages = [p for p in pkgutil.walk_packages([modules_path])]

    modules = []
    if hasattr(sys, 'frozen') and sys.frozen:
        for pkg in packages:
            # TODO
            try:
                module = pkg[0].load_module(pkg[1])
            except ImportError:
                print '*Invalid module', pkg[1]
            else:
                modules.append(module)
    else:
        for pkg in packages:
            if pkg[1].startswith('_'):
                print '*Ignored module', pkg[1]
                continue
            mod = ModuleWrapper(pkg[1], modules_path)
            find = mod.find()
            if find is None:
                print '*Invalid module', mod.name
            elif not find:
                print '*No config module for', mod.name
            else:
                mod.load()
            print '*Loading DB Objects', mod.name
            if not mod.load_database_objects():
                print '*DB Objects missing'
            if mod.valid:
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
            print '*** Missing dependencies for module', mod.name, ':', ' '.join(missing)
            raise Exception, 'Missing dependency'

def isInstalled(module_name):
    return (module_name in [mod.name for mod in modules])

# DATABASE EXTENSION

def configDB():
    print '*Clearing database...'
    pos.database.clear()
    print '*Re-creating database'
    pos.database.create()

def configTestDB():
    print '*Adding test values to database...'
    for mod in modules:
        try:
            test = mod.module.test_database_values
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
            item = mod.module.ModuleMenu
        except AttributeError:
            print '*Menu Extension missing', mod.name
        else:
            items.append(item(menu))

    for item in items:
        item.loadSubItems()
