import wx

from pos.modules.base.objects.idManager import ids

class EditDialog(wx.Dialog):
    def __init_ctrls(self):
        self.descriptionLbl = wx.StaticText(self, -1, label='Description')
        self.descriptionTxt = wx.TextCtrl(self, -1)
        self.descriptionTxt.SetValidator(EditValidator(self, 'description'))
        
        self.sellPriceLbl = wx.StaticText(self, -1, label='Sell Price')
        self.sellPriceTxt = wx.TextCtrl(self, -1)
        self.sellPriceTxt.SetValidator(EditValidator(self, 'sell_price'))
        
        self.amountLbl = wx.StaticText(self, -1, label='Amount')
        self.amountSpin = wx.SpinCtrl(self, -1, style=wx.SP_ARROW_KEYS, min=1)
        self.amountSpin.SetValidator(EditValidator(self, 'amount'))

        self.okBtn = wx.Button(self, wx.ID_OK, label='OK')
        self.cancelBtn = wx.Button(self, wx.ID_CANCEL, label='Cancel')
    
    def __init_sizers(self):
        self.formSizer = wx.GridBagSizer(hgap=5, vgap=5)
        
        fields = [(self.descriptionLbl, self.descriptionTxt),
                  (self.sellPriceLbl, self.sellPriceTxt),
                  (self.amountLbl, self.amountSpin)]
        for row, f in enumerate(fields):
            self.formSizer.Add(f[0], (row, 0), flag=wx.EXPAND | wx.ALL)
            self.formSizer.Add(f[1], (row, 1))
        self.formSizer.AddGrowableCol(1, 1)

        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL)
        self.controlSizer.Add(self.okBtn, 0, flag=wx.CENTER | wx.ALL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL)
        self.controlSizer.Add(self.cancelBtn, 0, flag=wx.CENTER | wx.ALL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL) 
        
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.AddSizer(self.formSizer, 1, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.AddSizer(self.controlSizer, 0, border=10, flag=wx.BOTTOM | wx.LEFT | wx.RIGHT | wx.EXPAND)
        self.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self)
    
    def __init__(self, parent, data):
        wx.Dialog.__init__(self, parent, ids['editTicketlineDialog'],
              size=wx.Size(400, 500), title='Edit ticketline')

        self.data = data
        self.__init_ctrls()
        self.__init_sizers()

class EditValidator(wx.PyValidator):
    def __init__(self, dialog, key):
        wx.PyValidator.__init__(self)
        self.dialog = dialog
        self.key = key

    Clone = lambda self: EditValidator(self.dialog, self.key)

    def Validate(self, parent):
        win = self.GetWindow()
        return True

    def TransferToWindow(self):
        try:
            win = self.GetWindow()
            data = self.dialog.data[self.key]
            if self.key == 'description':
                win.SetValue(data)
            elif self.key == 'sell_price':
                win.SetValue(str(data))
            elif self.key == 'amount':
                win.SetValue(data)
        except:
            print '-- ERROR -- in EditValidator.TransferToWindow'
            print '--', self.key, self.dialog.data
            raise
        return True

    def TransferFromWindow(self):
        try:
            win = self.GetWindow()
            if self.key == 'description':
                data = win.GetValue()
            elif self.key == 'sell_price':
                data = float(win.GetValue())
            elif self.key == 'amount':
                data = win.GetValue()
            self.dialog.data[self.key] = data
        except:
            print '-- ERROR -- in EditValidator.TransferFromWindow'
            print '--', self.key, self.dialog.data
            raise
        return True
