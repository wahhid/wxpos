import wx

import pos

import pos.modules.user.objects.permission as permission
from pos.modules.user.objects.permission import Permission, MenuRestriction

from pos.modules.user.windows import CheckTreeCtrl, CT_AUTO_CHECK_CHILD

from pos.modules.base.panels import ManagePanel

class PermissionsPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)
        
        self._init_panel('Permissions', DataValidator)
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Description', wx.TextCtrl, 'description', '',
                         style=wx.TE_MULTILINE)
        self.createField('Menu Restrictions', CheckTreeCtrl, 'menu_restrictions', [],
                         style=wx.TR_DEFAULT_STYLE | CT_AUTO_CHECK_CHILD | wx.TR_MULTIPLE,
                         size=(200, 200))
        self._init_fields()

    getItems = lambda self: pos.database.session().query(Permission, Permission.name).all()
    newItem = lambda self: permission.add(**self.data)
    updateItem = lambda self, p: p.update(**self.data)
    #def updateItem(self, p):
    #    data = self.data.copy()
    #    self.data.pop('menu_restrictions')
    #    p.update(**data)
    canEditItem = lambda self, p: True
    canDeleteItem = lambda self, p: len(p.roles) == 0
    
    def fillData(self):
        #tree = self.getField('menu_restrictions')
        #tree.DeleteAllItems()
        #root = tree.AddRoot('Menu')
        #for item in pos.menu.getItems():
        #    parent = tree.AppendItem(root, item.label)
        #    for i in item.children:
        #        child = tree.AppendItem(parent, i.label)
        #tree.Expand(root)
        p = self.getCurrentItem()
        if p is None: return
        self.getField('name').Enable(False)
        p.fillDict(self.data)

class DataValidator(wx.PyValidator):
    def __init__(self, panel, key):
        wx.PyValidator.__init__(self)
        self.panel = panel
        self.key = key

    Clone = lambda self: DataValidator(self.panel, self.key)

    def Validate(self, parent):
        try:
            win = self.GetWindow()
            data = self.getData(win)
            if self.key == 'name':
                return len(data) > 0
            elif self.key == 'description':
                return True
            elif self.key == 'menu_restrictions':
                return len(data) > 0
        except:
            print '-- ERROR -- in DataValidator.TransferToWindow'
            print '--', self.key, self.panel.data
            raise
        return True

    def TransferToWindow(self):
        try:
            win = self.GetWindow()
            data = self.panel.data[self.key]
            if self.key in ('name', 'description'):
                win.SetValue(data)
            elif self.key == 'menu_restrictions':
                restrictions = [(mr.root, mr.item) for mr in data]
                win.DeleteAllItems()
                items = {}
                root = win.AddRoot('Menu')
                for item in pos.menu.getItems():
                    parent = win.AppendItem(root, item.label)
                    for i in item.children:
                        child = win.AppendItem(parent, i.label)
                        items[item.label, i.label] = child
                win.Expand(root)
                for key, item in items.iteritems():
                    checked = (key in restrictions)
                    win.CheckItem(item, checked)
        except:
            print '-- ERROR -- in DataValidator.TransferToWindow'
            print '--', self.key, self.panel.data
            raise
        return True

    def TransferFromWindow(self):
        try:
            win = self.GetWindow()
            data = self.getData(win)
            self.panel.data[self.key] = data
        except:
            print '-- ERROR -- in DataValidator.TransferFromWindow'
            print '--', self.key, self.panel.data
            raise
        return True
        
    def getData(self, win):
        data = None
        if self.key in ('name', 'description'):
            data = win.GetValue()
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
