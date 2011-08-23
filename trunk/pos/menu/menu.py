class Menu:
    def __init__(self):
        self.items = {}

    def getItems(self):
        items = self.items.copy()
        
        main = items.pop('Main')
        system = items.pop('System')
        administration = items.pop('Administration')
        sub = items.values()
        return [main]+sub+[system, administration]
    
    def addRoot(self, item):
        self.items[item.label] = item
