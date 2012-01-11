import pos
from pos.modules import Module

class ModuleLoader(Module):
    name = 'Base Module'

    def menu(self):
        from pos.modules.base.panels import MainConfigPanel
            
        return [[{'label': 'Main', 'rel': 0, 'priority':5},
                 {'label': 'System', 'rel': -1, 'priority':4},
                 {'label': 'Administration', 'rel': -1, 'priority': 5}],
                [{'parent': 'System', 'label': 'Configuration', 'page': MainConfigPanel}]]
