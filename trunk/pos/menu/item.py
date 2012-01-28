class MenuItem:
    """
    A MenuItem is the item that is displayed in the secondary toolbook or
    directly inside the page of the main toolbook if alone.
    It always has a parent MenuRoot and a page associated to it.
    """
    def __init__(self, menu, parent, label, page, rel=0, priority=-1):
        self.parent = menu.items[parent]
        self.parent.addChild(self)
        
        self.label = label
        self.image_name = './res/menu/images/%s.png' % ((self.parent.label+'-'+self.label).lower(),)
        
        self.rel = rel
        self.priority = priority
        
        self.enabled = True
        
        self.page = page

    def __repr__(self):
        return '<MenuItem %s parent=%s>' %  (self.label, self.parent.label)
