import wx

import pos

from pos.modules.customer.objects.group import CustomerGroup

from pos.modules.base.panels import ManagePanel
from pos.modules.base.objects import validator as base_validator
from pos.modules.base.objects.formatter import TextFormatter

class CustomerGroupsPanel(ManagePanel):
    def __init__(self, parent):
        ManagePanel.__init__(self, parent, -1, 'Customer Groups', CustomerGroup, DataValidator)
        
        self.createField('Name', wx.TextCtrl, 'name', '', formatter=TextFormatter(required=True))
        self.createField('Comment', wx.TextCtrl, 'comment', '', formatter=TextFormatter(required=False),
                         style=wx.TE_MULTILINE)
        self._init_fields()

    canEditItem = lambda self, cg: True
    canDeleteItem = lambda self, cg: True

class DataValidator(base_validator.BaseValidator):
    def GetWindowData(self):
        win = self.GetWindow()
        if self.key == 'name':
            return win.GetValue()
        elif self.key == 'comment':
            return win.GetValue()
    
    def ValidateWindowData(self, data):
        return True
    
    def SetWindowData(self, data):
        win = self.GetWindow()
        if self.key == 'name':
            win.SetValue(data)
        elif self.key == 'comment':
            win.SetValue(data)
