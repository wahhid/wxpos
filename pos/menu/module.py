class ModuleMenuBase:
    """
    Wrapper class that only defines the functions used by a module
    to define the root items and menu items.
    ModuleMenu classes are not necessarily subclasses of this class, but these two functions are necessary.
    """
    def __init__(self, menu):
        self.menu = menu

    def loadSubItems(self):
        """
        This function should load all sub-items of the root items.
        It has to be defined in the subclass. Does nothing by default.
        """
        pass
