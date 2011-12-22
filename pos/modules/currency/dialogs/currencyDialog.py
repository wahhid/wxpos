import wx

import pos

class CurrencyDialog(wx.Dialog):
    def __init_ctrls(self):
        self.nameLbl = wx.StaticText(self, -1, label='Name')
        self.nameTxt = wx.TextCtrl(self, -1)
        self.nameTxt.SetValidator(DataValidator(self, 'name'))
        
        self.symbolLbl = wx.StaticText(self, -1, label='Symbol')
        self.symbolTxt = wx.TextCtrl(self, -1)
        self.symbolTxt.SetValidator(DataValidator(self, 'symbol'))
        
        self.valueLbl = wx.StaticText(self, -1, label='Value')
        self.valueTxt = wx.TextCtrl(self, -1)
        self.valueTxt.SetValidator(DataValidator(self, 'value'))
        
        self.decimalPlacesLbl = wx.StaticText(self, -1, label='Decimal Places')
        self.decimalPlacesSpin = wx.SpinCtrl(self, -1, style=wx.SP_ARROW_KEYS, min=0)
        self.decimalPlacesSpin.SetValidator(DataValidator(self, 'decimal_places'))

        self.digitGroupingLbl = wx.StaticText(self, -1, label='Digit Grouping')
        self.digitGroupingCb = wx.CheckBox(self, -1)
        self.digitGroupingCb.SetValidator(DataValidator(self, 'digit_grouping'))

        self.okBtn = wx.Button(self, wx.ID_OK, label='OK')
        self.cancelBtn = wx.Button(self, wx.ID_CANCEL, label='Cancel')
    
    def __init_sizers(self):
        self.formSizer = wx.GridBagSizer(hgap=5, vgap=5)
        
        fields = [(self.nameLbl, self.nameTxt),
                  (self.symbolLbl, self.symbolTxt),
                  (self.valueLbl, self.valueTxt),
                  (self.decimalPlacesLbl, self.decimalPlacesSpin),
                  (self.digitGroupingLbl, self.digitGroupingCb)]
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
    
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1,
              size=wx.Size(400, 500), title='Create Currency')

        self.data = {}
        self.__init_ctrls()
        self.__init_sizers()
    
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
            if self.key in ('name', 'symbol'):
                return len(data)>0
            elif self.key == 'decimal_places':
                return True
            elif self.key == 'digit_grouping':
                return True
            elif self.key == 'value':
                try:
                    float(data)
                except:
                    return False
        except:
            print '-- ERROR -- in DataValidator.TransferToWindow'
            print '--', self.key, self.panel.data
            raise
        return True

    def TransferToWindow(self):
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
        if self.key in ('name', 'symbol', 'value', 'decimal_places', 'digit_grouping'):
            data = win.GetValue()
        return data
