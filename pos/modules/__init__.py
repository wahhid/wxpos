import pos
import imp, os, sys
import pkgutil

class ModuleWrapper:
    def __init__(self, pkg, parent):
        self.package = pkg
        self.name = pkg[1]
        self.parent = parent
        self.cfg = None
        self.top_pathname = None
        self.valid = None
        self.dependencies = []

    def find(self):
        if hasattr(sys, 'frozen') and sys.frozen:
            for pkg in pkgutil.iter_modules([os.path.join(self.parent, self.package[1])]):
                if pkg[1] == 'config':
                    self.cfg = pkg
                    self.valid = True
                    break
            else:
                self.valid = False
            return self.valid
        else:
            try:
                _file, self.top_pathname, description = imp.find_module(self.name, [self.parent])
            except ImportError as e:
                self.valid = False
                return None
            else:
                try:
                    self.cfg = imp.find_module('config', [self.top_pathname])
                except ImportError as e:
                    self.valid = False
                    return False
                else:
                    self.valid = True
                    return True
                return self.valid

    def load(self):
        if not self.valid: return
        if hasattr(sys, 'frozen') and sys.frozen:
            self.top_module = self.package[0].load_module(self.package[1])
            self.module = self.cfg[0].load_module(self.name+'.'+self.cfg[1])
        else:
            self.top_module = imp.load_package(self.name, self.top_pathname)
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

    def init(self):
        if not self.valid: return
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
        find = mod.find()
        if find is None:
            print '*Invalid module', mod.name
        elif not find:
            print '*No config module for', mod.name
        else:
            mod.load()
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
