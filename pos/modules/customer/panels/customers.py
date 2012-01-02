import wx

import pos

import pos.modules.currency.objects.currency as currency
from pos.modules.currency.objects.currency import Currency

from pos.modules.customer.objects.customer import Customer
from pos.modules.customer.objects.group import CustomerGroup
from pos.modules.customer.objects.contact import CustomerContact
from pos.modules.customer.objects.address import CustomerAddress

from pos.modules.customer.windows import ContactCtrl, AddressCtrl

from pos.modules.base.panels import ManagePanel
from pos.modules.base.objects import validator as base_validator
from pos.modules.base.objects.formatter import FloatFormatter, TextFormatter, AlphaNumericFormatter

class CustomersPanel(ManagePanel):
    def __init__(self, parent):
        ManagePanel.__init__(self, parent, -1, 'Customers', Customer, DataValidator)
        
        self.createField('Name', wx.TextCtrl, 'name', '', formatter=TextFormatter(required=True))
        self.createField('Code', wx.TextCtrl, 'code', None, formatter=AlphaNumericFormatter(required=False))
        self.createField('First Name', wx.TextCtrl, 'first_name', None, formatter=TextFormatter(required=False))
        self.createField('Last Name', wx.TextCtrl, 'last_name', None, formatter=TextFormatter(required=False))
        self.createField('General Discount', wx.SpinCtrl, 'discount', 0, formatter=FloatFormatter(required=True),
                         min=0, max=100)
        self.createField('Max Debt', wx.TextCtrl, 'max_debt', None, formatter=FloatFormatter(required=False))
        self.createField('Preferred Currency', wx.Choice, 'currency', currency.get_default())
        self.createField('Groups', wx.CheckListBox, 'groups', [])
        self.createField('Comment', wx.TextCtrl, 'comment', '',
                         style=wx.TE_MULTILINE)
        self.createField('Contact', ContactCtrl, 'contacts', [])
        self.createField('Address', AddressCtrl, 'addresses', [])
        self._init_fields()

    canEditItem = lambda self, c: True
    canDeleteItem = lambda self, c: True

    def newItem(self):
        data = self.formPanel.data
        for i, c in enumerate(data['contacts']):
            if type(c) == dict:
                data['contacts'][i] = CustomerContact(customer=None, **c)
        for i, a in enumerate(data['addresses']):
            if type(a) == dict:
                data['addresses'][i] = CustomerAddress(customer=None, **a)
        return ManagePanel.newItem(self)
    
    def updateItem(self, item):
        data = self.formPanel.data
        contacts_data = data['contacts'].copy()
        data['contacts'] = []
        for c, D in contacts_data:
            if c is None:
                data['contacts'].append(CustomerContact(customer=item, **D))
            else:
                data['contacts'].append(c)
        
        addresses_data = data['addresses'].copy()
        data['addresses'] = []
        for a, D in addresses_data:
            if a is None:
                data['addresses'].append(CustomerAddress(customer=item, **D))
            else:
                data['addresses'].append(a)
        
        return ManagePanel.updateItem(self, item)

class DataValidator(base_validator.BaseValidator):
    def GetWindowData(self):
        win = self.GetWindow()
        if self.key == 'name':
            return win.GetValue()
        elif self.key in ('code', 'first_name', 'last_name'):
            data = win.GetValue()
            if data == '':
                data = None
            return data
        elif self.key == 'comment':
            return win.GetValue()
        elif self.key == 'max_debt':
            data = win.GetValue()
            if data == '':
                data = None
            return data
        elif self.key == 'discount':
            return win.GetValue()/100.0
        elif self.key == 'groups':
            checked_groups_txt = win.CheckedStrings
            session = pos.database.session()
            return session.query(CustomerGroup).filter(CustomerGroup.display.in_(checked_groups_txt)).all()
        elif self.key == 'currency':
            currency_symbol = win.GetStringSelection()
            session = pos.database.session()
            return session.query(Currency).filter_by(symbol=currency_symbol).one()
        elif self.key == 'contacts':
            return win.GetValue()
        elif self.key == 'addresses':
            return win.GetValue()
    
    def ValidateWindowData(self, data):
        if self.key == 'addresses':
            if not self.panel.getField('addresses').addressPanel.Validate():
                return False
        elif self.key == 'contacts':
            # TODO Validate the ContactCtrl
            return True
        return True
    
    def SetWindowData(self, data):
        win = self.GetWindow()
        if self.key == 'name':
            win.SetValue(data)
        elif self.key in ('code', 'first_name', 'last_name'):
            if data is None:
                win.SetValue('')
            else:
                win.SetValue(data)
        elif self.key == 'comment':
            win.SetValue(data)
        elif self.key == 'max_debt':
            if data is None:
                win.SetValue('')
            else:
                win.SetValue(str(data))
        elif self.key == 'discount':
            win.SetValue(data*100.0)
        elif self.key == 'groups':
            session = pos.database.session()
            groups_txt = session.query(CustomerGroup.display).all()
            win.Set([cg[0] for cg in groups_txt])
            
            checked_indices = []
            for cg in data:
                index = win.FindString(cg.display)
                checked_indices.append(index)
            for i in range(win.GetCount()):
                win.Check(i, i in checked_indices)
        elif self.key == 'currency':
            session = pos.database.session()
            currency_choices = session.query(Currency.symbol).all()
            win.SetItems([c[0] for c in currency_choices])
            if data is not None:
                win.SetStringSelection(data.symbol)
            else:
                win.SetSelection(-1)
        elif self.key == 'contacts':
            win.SetValue(data)
        elif self.key == 'addresses':
            win.SetValue(data)
