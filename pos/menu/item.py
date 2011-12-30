class MenuItem:
    """
    A MenuItem is the item that is displayed in the secondary toolbook or
    directly inside the page of the main toolbook if alone.
    It always has a parent MenuRoot and a page associated to it.
    """
    def __init__(self, menu, parent, label, page):
        self.parent = menu.items[parent]
        self.parent.addChild(self)
        
        self.label = label
        self.image_name = 'images/menu/'+self.parent.label+'-'+self.label+'.png'
        
        self.page = page

    def __repr__(self):
        return '<MenuItem %s parent=%s>' %  (self.label, self.parent.label)
