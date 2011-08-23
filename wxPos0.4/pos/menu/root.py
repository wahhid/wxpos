class MenuRoot:
    def __init__(self, menu, label, perm=None):
        self.menu = menu
        self.label = label
        self.children = []
        self.perm = perm
        self.image_name = 'images/menu/'+self.label+'.png'
        
        menu.addRoot(self)
    
    def addChild(self, child):
        self.children.append(child)
