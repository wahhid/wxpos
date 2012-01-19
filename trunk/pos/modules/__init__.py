import pos

pos.config.set_default('mod', 'disabled_modules', '')

import os, sys
import pkgutil, importlib

class Module:
    name = None
    dependencies = tuple()
    config = []
    
    def __init__(self, base_name):
        self.base_name = base_name
        if self.name is None:
            self.name = self.base_name.title()
        
        self.__bindings = {}
        
        for section, options in self.config:
            for opt, val in options.iteritems():
                pos.config.set_default(section, opt, val)
        
        self.event_handler()
    
    def load(self):
        return []
    
    def test(self):
        pass
    
    def menu(self):
        return [[], []]
    
    def init(self):
        return True
    
    def event_handler(self):
        pass
    
    def bind_event(self, type_, callback):
        self.__bindings[type_] = callback
    
    def handle_event(self, evt):
        if evt.target is not None and self.base_name != self.type and \
            not (type(evt.type) in (list, tuple) and self.base_name in evt.type):
            return True
        try:
            callback = self.__bindings[evt.type]
        except KeyError:
            return True
        return callback(evt)
    
    def __lt__(self, mod):
        """
        Implements the '<' comparison operator.
        Used when sorting the list of modules, by dependencies.
        """
        return (self.base_name in mod.dependencies)
    
    def __repr__(self):
        return '<Module %s>' % (self.base_name,)

class ModuleWrapper:
    """
    Wrapper around the actual installed module.
    Provides functions to make common tasks easier.
    """
    def __init__(self, package):
        self.package = package
        self.name = package[1]
        
        self.loader = None
        self.disabled = False
        self.forced_disable = False

    def load(self):
        """
        This will load the main module and initiate the ModuleLoader class 
        """
        if self.disabled:
            return False
        self.top_module = importlib.import_module('pos.modules.'+self.name)
        if self.top_module is None:
            return False
        try:
            self.loader = self.top_module.ModuleLoader(self.name)
        except AttributeError:
            return False
        all_modules.append(self)
        return True
    
    def disable(self, missing_dependency=False):
        global disabled_modules, missing_modules
        self.disabled = True
        sys.modules['pos.modules.'+self.name] = None
        if missing_dependency:
            self.forced_disable = True
            missing_modules.append(self)
        else:
            self.forced_disable = False
            disabled_modules.append(self)
    
    def uninstall(self):
        raise NotImplementedError, 'Uninstall a module is not yet supported.'
    
    def __repr__(self):
        return '<ModuleWrapper %s>' % (self.name, )

all_modules = []
disabled_modules = []
missing_modules = []
missing_dependencies = set()
module_loaders = []

def init():
    """
    Load all the modules installed (main and config).
    """
    global module_loaders
    
    disabled_str = pos.config['mod', 'disabled_modules']
    disabled_names = disabled_str.split(',') if disabled_str != '' else []
    
    print '*Loading modules...'
    modules_path = os.path.dirname(__file__)
    # Package with names starting with '_' are ignored
    packages = [p for p in pkgutil.walk_packages([modules_path]) if not p[1].startswith('_') and p[2]]
    
    for pkg in packages:
        mod = ModuleWrapper(pkg)
        if mod.name in disabled_names:
            mod.disable()
            continue
        print '*Loading module', mod.name
        if not mod.load():
            print '*Invalid module', mod.name
    print '*(%d) modules found: %s' % (len(all_modules), ', '.join([m.name for m in all_modules]))
    if disabled_modules:
        print '*(%d) modules disabled: %s' % (len(disabled_modules), ', '.join([m.name for m in disabled_modules]))
    _checkModuleDependencies()
    if missing_modules:
        print '*(%d) modules disabled for missing dependencies: %s' % (len(missing_modules), ', '.join([m.name for m in missing_modules]))
    
    module_loaders = [mod.loader for mod in all_modules if not mod.disabled]
    module_loaders.sort()

def _checkModuleDependencies():
    print '*Checking module dependencies...'
    to_remove = []
    module_names = set(mod.name for mod in all_modules)
    for mod in all_modules:
        missing = set(mod.loader.dependencies)-module_names
        if missing:
            missing_dependencies.update(missing)
            print '*Missing dependencies for module', mod.name, ':', ', '.join(missing)
            to_remove.append(mod)
    if not to_remove: return
    
    def iter_to_remove(remove_list, remove_set=set()):
        remove_set.update(remove_list)
        for mod in remove_list:
            used_in_set = set(m for m in all_modules if mod.name in m.loader.dependencies)
            iter_to_remove(used_in_set - remove_set, remove_set)
        return list(remove_set)
    
    [mod.disable(missing_dependency=True) for mod in iter_to_remove(to_remove)]

def isInstalled(module_name):
    """
    Returns True if the module called module_name is installed.
    """
    for mod in all_modules:
        if module_name == mod.name:
            return True
    return False

def all():
    """
    Returns a tuple of all the Module objects that are linked to all the actual modules installed.
    """
    return tuple(module_loaders)

def all_wrappers():
    """
    Returns a tuple of all the ModuleWrapper objects that are linked to all the actual modules installed.
    """
    return all_modules+disabled_modules+missing_modules

# DATABASE EXTENSION

def loadDB():
    """
    Load all the database objects of every module so that they can be used with SQLAlchemy.
    """
    for mod in module_loaders:
        print '*Loading DB Objects', '%s.' % (mod.base_name,),
        objects = mod.load()
        print len(objects), 'found'

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
    for mod in module_loaders:
        print '*Adding Test Values', mod.base_name
        mod.test()

# MENU EXTENSION

def extendMenu(menu):
    """
    Load all menu extensions of every module, meaning all the root items and sub-items defined.
    """
    from pos.menu import MenuRoot, MenuItem
    roots = []
    items = []
    for mod in module_loaders:
        mod_roots, mod_items = mod.menu()
        roots.extend(mod_roots)
        items.extend(mod_items)

    for root in roots:
        MenuRoot(menu, **root)

    for item in items:
        MenuItem(menu, **item)
