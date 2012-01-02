import wx

import pos

from pos.modules.customer.objects.address import CustomerAddress

from pos.modules.base.panels import FormPanel
from pos.modules.base.objects import validator as base_validator

class AddressCtrl(wx.PyPanel):
    def __init__(self, parent, id):
        wx.PyPanel.__init__(self, parent, id)
        self.__addresses = {}
        self.index = -1
        self.__selection = -1
        
        self.addBtn = wx.Button(self, -1, '+')
        self.addBtn.Bind(wx.EVT_BUTTON, self.OnAddButton)
        
        self.addressChoice = wx.Choice(self, -1)
        self.addressChoice.Bind(wx.EVT_CHOICE, self.OnAddressChoice)
        
        self.removeBtn = wx.Button(self, -1, '-')
        self.removeBtn.Bind(wx.EVT_BUTTON, self.OnRemoveButton)
        
        self.addressPanel = AddressPanel(self, -1)
        
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.Add(self.addBtn, 0)
        self.mainSizer.Add(self.addressChoice, 0)
        self.mainSizer.Add(self.removeBtn, 0)
        self.mainSizer.Add(self.addressPanel, 1, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.mainSizer)
    
    def OnAddressChoice(self, event):
        event.Skip()
        selection = self.addressChoice.GetSelection()
        if selection == -1: return
        index = self.addressChoice.GetClientData(selection)
        
        self.saveChanges()
        self.__selection = selection
        
        self.addressPanel.fillForm(item=None, data=self.__addresses[index]['data'])
    
    def saveChanges(self):
        selection = self.__selection#self.addressChoice.GetSelection()
        if selection == -1: return
        index = self.addressChoice.GetClientData(selection)
        
        self.addressPanel.TransferDataFromWindow()
        self.__addresses[index]['data'] = self.addressPanel.data.copy()
    
    def OnAddButton(self, event):
        event.Skip()
        self.addressPanel.resetForm()
        self.index += 1
        self.__addresses[self.index] = {'address': None, 'data': self.addressPanel.data.copy(), 'removed': False}
        string = '[New Address %d]' % (self.index,)
        self.addressChoice.Append(string, self.index)
        self.addressChoice.SetStringSelection(string)
    
    def OnRemoveButton(self, event):
        event.Skip()
        selection = self.addressChoice.GetSelection()
        if selection == -1: return
        index = self.addressChoice.GetClientData(selection)
        self.__addresses[index]['removed'] = True
        self.__selection = -1
        self.addressChoice.Delete(selection)
        
        self.addressChoice.SetSelection(-1)
        self.addressPanel.resetForm()
    
    def SetValue(self, addresses):
        self.__addresses = {}
        self.index = -1
        self.__selection = -1
        self.addressChoice.SetItems([])
        self.addressChoice.SetSelection(-1)
        self.addressPanel.resetForm()
        default_data = self.addressPanel.data.copy()
        for a in addresses:
            self.index += 1
            data = default_data.copy()
            a.fillDict(data)
            self.__addresses[self.index] = {'address': a, 'data': data.copy(),'removed': False}
            self.addressChoice.Append(a.display, self.index)
    
    def GetValue(self):
        self.saveChanges()
        addresses = []
        for D in self.__addresses.itervalues():
            if D['removed']: continue
            addresses.append((D['address'], D['data']))
        return addresses

class AddressPanel(FormPanel):
    def __init__(self, parent, id):
        FormPanel.__init__(self, parent, id, AddressValidator)
        
        self.createField('Country', wx.TextCtrl, 'country', '')
        self.createField('Region', wx.TextCtrl, 'region', '')
        self.createField('City', wx.TextCtrl, 'city', '')
        self.createField('Details', wx.TextCtrl, 'details', '')
        self._init_fields()

class AddressValidator(base_validator.BaseValidator):
    def GetWindowData(self):
        win = self.GetWindow()
        if self.key in ('country', 'region', 'city', 'details'):
            return win.GetValue()
    
    def ValidateWindowData(self, data):
        return True
    
    def SetWindowData(self, data):
        win = self.GetWindow()
        if self.key in ('country', 'region', 'city', 'details'):
            return win.SetValue(data)
