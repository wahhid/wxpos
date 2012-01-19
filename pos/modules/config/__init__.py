import pos
from pos.modules import Module

class ModuleLoader(Module):
    dependencies = ('base',)
    name = 'Configuration Interface Module'

    def menu(self):
        from pos.modules.config.panels import MainConfigPanel
            
        return [[],
                [{'parent': 'System', 'label': 'Configuration', 'page': MainConfigPanel}]]
