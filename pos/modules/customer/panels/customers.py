import wx

from pos.modules.base.objects.idManager import ids

import pos.modules.customer.objects.customergroup as customergroup
import pos.modules.customer.objects.customer as customer

from pos.modules.base.panels import ManagePanel

class CustomersPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, id=ids['customersPanel'], parent=parent, style=wx.TAB_TRAVERSAL)
        
        self._init_panel('Customers', DataValidator)
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Code', wx.TextCtrl, 'code', None)
        self.createField('First Name', wx.TextCtrl, 'first_name', None)
        self.createField('Last Name', wx.TextCtrl, 'last_name', None)
        self.createField('Max Debt', wx.TextCtrl, 'max_debt', None)
        self.createField('Groups', wx.CheckListBox, 'groups', [])
        self.createField('Comment', wx.TextCtrl, 'comment', None,
                         style=wx.TE_MULTILINE)
        self._init_fields()

    getItems = lambda self: [{'text': p.data['name']} for p in customer.find(list=True)]
    getItem = lambda self, item: customer.find(name=item.GetText())
    newItem = lambda self: customer.add(**self.data)
    updateItem = lambda self, c: c.update(**self.data)
    canEditItem = lambda self, c: True
    canDeleteItem = lambda self, c: True
    
    def fillData(self):
        self.getField('groups').Set(map(lambda cg: cg.data['name'], customergroup.find(list=True)))
        c = self.getCurrentItem()
        if c is None: return
        self.data = c.data.copy()

class DataValidator(wx.PyValidator):
    def __init__(self, panel, key):
        wx.PyValidator.__init__(self)
        self.panel = panel
        self.key = key

    Clone = lambda self: DataValidator(self.panel, self.key)

    def Validate(self, parent):
        win = self.GetWindow()
        return True

    def TransferToWindow(self):
        try:
            win = self.GetWindow()
            data = self.panel.data[self.key]
            if self.key == 'name':
                win.SetValue(data)
            elif self.key in ('code', 'first_name', 'last_name', 'comment'):
                if data is None:
                   win.SetValue('')
                else:
                    win.SetValue(data)
            elif self.key == 'max_debt':
                if data is None:
                   win.SetValue('')
                else:
                    win.SetValue(str(data))
            elif self.key == 'groups':
                checked_indices = []
                for cg in data:
                    index = win.FindString(cg.data['name'])
                    checked_indices.append(index)
                for i in range(win.GetCount()):
                    win.Check(i, i in checked_indices)
        except:
            print '-- ERROR -- in DataValidator.TransferToWindow'
            print '--', self.key, self.panel.data
            raise
        return True

    def TransferFromWindow(self):
        try:
            win = self.GetWindow()
            if self.key == 'name':
                data = win.GetValue()
            elif self.key in ('code', 'first_name', 'last_name', 'comment'):
                data = win.GetValue()
                if data == '':
                    data = None
            elif self.key == 'max_debt':
                data = win.GetValue()
                if data == '':
                    data = None
            elif self.key == 'groups':
                data = map(lambda cgname: customergroup.find(name=cgname), win.CheckedStrings)
            self.panel.data[self.key] = data
        except:
            print '-- ERROR -- in DataValidator.TransferFromWindow'
            print '--', self.key, self.panel.data
            raise
        return True
