import pos
from pos.modules import Module

class ModuleLoader(Module):
    dependencies = ('base',)
    name = 'Module Installer and Manager'

    def event_handler(self):
        pass
        #self.bind_event(pos.EVT_START, self.onStart)

    def menu(self):
        from pos.modules.installer.panels import ModulesPanel
            
        return [[],
                [{'parent': 'System', 'label': 'Modules', 'page': ModulesPanel}]]

    def init(self):
        # Check for updates
        return True

    def onStart(self, evt):
        print 'base', 'onStart ewewewweewewewew'
