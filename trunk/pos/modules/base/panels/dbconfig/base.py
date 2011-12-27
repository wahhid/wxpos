import wx

import pos

class DatabaseConfigPanel(wx.Panel):
    def initParam(self, config, validator):
        self.config = config
        self.validator = validator
        self.fields = {}
        self.field_order = []
    
    def addParam(self, name, label, wxObj, required=False, style=None):
        self.field_order.append(name)
        self.fields[name] = [None, None, None]
        enabled = required or pos.config[self.config, name] is not None
        
        self.fields[name][0] = wx.CheckBox(self, -1)
        self.fields[name][0].Bind(wx.EVT_CHECKBOX, lambda evt, n=name: self.OnCheckBox(evt, n))
        self.fields[name][0].SetValue(enabled)
        self.fields[name][0].Enable(not required)
        self.fields[name][1] = wx.StaticText(self, -1, label=label)
        if style is not None:
            self.fields[name][2] = wxObj(self, -1, style=style)
        else:
            self.fields[name][2] = wxObj(self, -1)
        self.fields[name][2].SetValidator(self.validator(self.config, name))
        self.fields[name][2].Enable(enabled)
        
    def getParam(self, name):
        return self.fields[name][2]

    def placeParam(self):
        self.mainSizer = wx.FlexGridSizer(rows=len(self.fields), cols=3)
        for name in self.field_order:
            for w in self.fields[name]:
                self.mainSizer.Add(w, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.mainSizer)
    
    def OnCheckBox(self, event, name):
        event.Skip()
        self.getParam(name).Enable(self.fields[name][0].IsChecked())
    
    def __init__(self, parent, config, validator=None):
        wx.Panel.__init__(self, parent, -1)
        
        val = ConfigValidator if validator is None else validator
        self.initParam(config, val)

class ConfigValidator(wx.PyValidator):
    def __init__(self, config, key):
        wx.PyValidator.__init__(self)
        self.key = key
        self.config = config

    Clone = lambda self: ConfigValidator(self.config, self.key)

    def Validate(self, parent):
        return True

    def TransferToWindow(self):
        win = self.GetWindow()
        if not win.IsEnabled() or pos.config[self.config, self.key] is None:
            return True
        data = pos.config[self.config, self.key]
        win.SetValue(data)
        return True

    def TransferFromWindow(self):
        win = self.GetWindow()
        if not win.IsEnabled():
            pos.config[self.config, self.key] = None
            return True
        pos.config[self.config, self.key] = win.GetValue()
        return True
