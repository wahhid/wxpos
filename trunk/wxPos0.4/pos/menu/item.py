class MenuItem:
    def __init__(self, menu, parent, label, page, perm=None):
        self.label = label
        self.perm = perm
        self.parent = menu.items[parent]
        self.page = page
        self.image_name = 'images/menu/'+self.parent.label+'-'+self.label+'.png'
        
        self.parent.addChild(self)
