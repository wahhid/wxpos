import wx

import pos

import pos.modules.currency.objects.currency as currency
from pos.modules.currency.objects.currency import Currency

import pos.modules.customer.objects.customer as customer
from pos.modules.customer.objects.customer import Customer
from pos.modules.customer.objects.customergroup import CustomerGroup

from pos.modules.base.panels import ManagePanel

class CustomersPanel(wx.Panel, ManagePanel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)
        
        self._init_panel('Customers', DataValidator)
        self.createField('Name', wx.TextCtrl, 'name', '')
        self.createField('Code', wx.TextCtrl, 'code', None)
        self.createField('First Name', wx.TextCtrl, 'first_name', None)
        self.createField('Last Name', wx.TextCtrl, 'last_name', None)
        self.createField('Max Debt', wx.TextCtrl, 'max_debt', None)
        self.createField('Preferred Currency', wx.Choice, 'currency', currency.get_default())
        self.createField('Groups', wx.CheckListBox, 'groups', [])
        self.createField('Comment', wx.TextCtrl, 'comment', None,
                         style=wx.TE_MULTILINE)
        self._init_fields()

    getItems = lambda self: pos.database.session().query(Customer, Customer.name).all()
    newItem = lambda self: customer.add(**self.data)
    updateItem = lambda self, c: c.update(**self.data)
    canEditItem = lambda self, c: True
    canDeleteItem = lambda self, c: True
    
    def fillData(self):
        session = pos.database.session()
        
        customergroup_names = session.query(CustomerGroup.name).all()
        self.getField('groups').Set([cg[0] for cg in customergroup_names])
        
        currency_choices = session.query(Currency.symbol).all()
        self.getField('currency').SetItems([c[0] for c in currency_choices])
        
        c = self.getCurrentItem()
        if c is None: return
        c.fillDict(self.data)

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
                    index = win.FindString(cg.name)
                    checked_indices.append(index)
                for i in range(win.GetCount()):
                    win.Check(i, i in checked_indices)
            elif self.key == 'currency':
                if data is not None:
                    win.SetStringSelection(data.symbol)
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
                session = pos.database.session()
                data = session.query(CustomerGroup).filter(CustomerGroup.name.in_(win.CheckedStrings)).all()
            elif self.key == 'currency':
                currency_symbol = win.GetStringSelection()
                session = pos.database.session()
                data = session.query(Currency).filter_by(symbol=currency_symbol).one()
            self.panel.data[self.key] = data
        except:
            print '-- ERROR -- in DataValidator.TransferFromWindow'
            print '--', self.key, self.panel.data
            raise
        return True
