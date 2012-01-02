import wx
from wx.lib.scrolledpanel import ScrolledPanel

import pos

class ContactCtrl(ScrolledPanel):
    def __init__(self, parent, id):
        ScrolledPanel.__init__(self, parent, id, size=(300, 150))
        self.index = -1
        self.__contacts = {}
        self.name_choices = ('email', 'phone', 'mobile', 'fax')
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        
        addBtn = wx.Button(self, -1, '+')
        addBtn.Bind(wx.EVT_BUTTON, self.OnAddButton)
        self.mainSizer.Add(addBtn)
        
        self.SetSizer(self.mainSizer)
        self.SetupScrolling()
    
    def AddRow(self, c):
        nameChoice = wx.Choice(self, -1, choices=self.name_choices)
        valueTxt = wx.TextCtrl(self, -1)
        removeBtn = wx.Button(self, -1, '-')
        
        sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        sizer.Add(nameChoice, border=5, flag=wx.ALL)
        sizer.Add(valueTxt, border=5, flag=wx.ALL)
        sizer.Add(removeBtn, border=5, flag=wx.ALL)
        
        self.mainSizer.Add(sizer, flag=wx.EXPAND | wx.ALL)
        
        if c is None:
            data = {'name': self.name_choices[0], 'value': ''}
        else:
            data = {'name': '', 'value': ''}
            c.fillDict(data)
        
        self.index += 1
        self.__contacts[self.index] = {'sizer': sizer, 'contact': None, 'data': data, 'removed': False}
        
        nameChoice.SetStringSelection(data['name'])
        valueTxt.SetValue(data['value'])
        removeBtn.Bind(wx.EVT_BUTTON, lambda event, i=self.index: self.OnRemoveButton(event, i))
        
        return self.index
    
    def RemoveRow(self, index):
        D = self.__contacts[index]
        D['sizer'].Clear(True)
        D['removed'] = True
    
    def OnRemoveButton(self, event, index):
        self.RemoveRow(index)
        self.mainSizer.Layout()
        self.SetupScrolling()
    
    def OnAddButton(self, event):
        event.Skip()
        self.AddRow(None)
        self.mainSizer.Layout()
        self.SetupScrolling()
    
    def SetValue(self, contacts):
        for i in self.__contacts.copy():
            self.RemoveRow(i)
        self.index = -1
        self.__contacts = {}
        for c in contacts:
            self.AddRow(c)
        self.mainSizer.Layout()
        self.SetupScrolling()
    
    def GetValue(self):
        contacts = []
        for D in self.__contacts.itervalues():
            if D['removed']: continue
            nameChoice = D['sizer'].GetItem(0).GetWindow()
            valueTxt = D['sizer'].GetItem(1).GetWindow()
            D['data']['name'] = nameChoice.GetStringSelection()
            D['data']['value'] = valueTxt.GetValue()
            contacts.append((D['contact'], D['data']))
        return contacts
