import pos
from pos.modules import Module

class ModuleLoader(Module):
    name = 'Base Module'

    def menu(self):
        return [[{'label': 'Main', 'rel': 0, 'priority':5},
                 {'label': 'System', 'rel': -1, 'priority':4},
                 {'label': 'Administration', 'rel': -1, 'priority': 5}],
                []]

    def config_panels(self):
        from pos.modules.base.panels import MenuConfigPanel
        from pos.modules.base.panels import AppConfigPanel
        return [AppConfigPanel, MenuConfigPanel]