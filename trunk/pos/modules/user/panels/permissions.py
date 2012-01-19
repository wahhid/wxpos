import wx

import pos

from pos.modules.user.objects.permission import Permission, MenuRestriction

from pos.modules.user.windows import CheckTreeCtrl, CT_AUTO_CHECK_CHILD

from pos.modules.base.panels import ManagePanel
from pos.modules.base.objects import validator as base_validator
from pos.modules.base.objects.formatter import TextFormatter

class PermissionsPanel(ManagePanel):
    def __init__(self, parent):
        ManagePanel.__init__(self, parent, -1, 'Permissions', Permission, DataValidator)
        
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Description', wx.TextCtrl, 'description', '',
                         formatter=TextFormatter(required=False),
                         style=wx.TE_MULTILINE)
        self.createField('Menu Restrictions', CheckTreeCtrl, 'menu_restrictions', [],
                         style=wx.TR_DEFAULT_STYLE | CT_AUTO_CHECK_CHILD | wx.TR_MULTIPLE,
                         size=(200, 200))
        self._init_fields()

    canEditItem = lambda self, p: True
    canDeleteItem = lambda self, p: len(p.roles) == 0

class DataValidator(base_validator.BaseValidator):
    def GetWindowData(self):
        win = self.GetWindow()
        if self.key in ('name', 'description'):
            return win.GetValue()
        elif self.key == 'menu_restrictions':
            checked = win.GetChecked()
            session = pos.database.session()
            data = []
            for i in checked:
                parent = win.GetItemParent(i)
                root = win.GetItemText(parent)
                item = win.GetItemText(i)
                try:
                    mr = session.query(MenuRestriction).filter_by(root=root, item=item).one()
                except:
                    mr = MenuRestriction(root=root, item=item)
                data.append(mr)
            return data
    
    def ValidateWindowData(self, data):
        if self.key == 'name':
            return (data != '')
        elif self.key == 'menu_restrictions':
            return (len(data)>0)
        return True
    
    def SetWindowData(self, data):
        win = self.GetWindow()
        if self.key == 'name':
            win.SetValue(data)
            if data != '':
                win.Enable(False)
            else:
                win.Enable(True)
        elif self.key == 'description':
            win.SetValue(data)
        elif self.key == 'menu_restrictions':
            restrictions = [(mr.root, mr.item) for mr in data]
            win.DeleteAllItems()
            items = {}
            root = win.AddRoot('Menu')
            for item in pos.menu.main.items:
                parent = win.AppendItem(root, item.label)
                for i in item.children:
                    child = win.AppendItem(parent, i.label)
                    items[item.label, i.label] = child
            win.Expand(root)
            for key, item in items.iteritems():
                checked = (key in restrictions)
                win.CheckItem(item, checked)
