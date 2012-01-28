class MenuRoot:
    """
    Root Menu Item that is displayed in the main toolbook
    and has one or many related children items.
    """
    def __init__(self, menu, label, rel=0, priority=-1):
        self.menu = menu
        self.label = label
        self.image_name = './res/menu/images/%s.png' % (self.label.lower(),)
        
        self.rel = rel
        self.priority = priority
        
        self.enabled = True
        
        self.children = []
        menu.addRoot(self)
    
    def addChild(self, child):
        self.children.append(child)

    def __repr__(self):
        return '<MenuRoot %s (%d,%d)>' %  (self.label, self.rel, self.priority)
