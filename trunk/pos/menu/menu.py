class Menu:
    """
    Holds the hierarchy of the menu system.
    Root items are associated to it, and items associated to a root item.
    """
    def __init__(self):
        self.items = {}

    def getItems(self):
        """
        Returns all the root items in the desired order, as close as possible
        to the one requested from the modules.
        """
        items = self.items.values()
        grouped = [[] for j in range(len(items))]
        ordered = []
        for i in items:
            pos = min(i.rel, len(items)-1) if i.rel>=0 else max(i.rel, -len(items))
            grouped[pos].append(i)
        for L in grouped:
            L.sort(key=lambda i: (-i.priority if i.rel>=0 else i.priority))
            ordered.extend(L)
        return ordered
    
    def addRoot(self, item):
        self.items[item.label] = item
    
    def __repr__(self):
        return '<Menu %d items>' %  (len(self.items),)
