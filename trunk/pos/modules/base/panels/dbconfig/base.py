import wx

import pos

class DatabaseConfigPanel(wx.Panel):
    def addParam(self, name, label, wxObj, required=False, style=None):
        self.field_order.append(name)
        self.fields[name] = [None, None, None]
        enabled = required
        
        self.fields[name][0] = wx.CheckBox(self, -1)
        self.fields[name][0].Bind(wx.EVT_CHECKBOX, lambda evt, n=name: self.OnCheckBox(evt, n))
        self.fields[name][0].SetValue(enabled)
        self.fields[name][0].Enable(not required)
        self.fields[name][1] = wx.StaticText(self, -1, label=label)
        if style is not None:
            self.fields[name][2] = wxObj(self, -1, style=style)
        else:
            self.fields[name][2] = wxObj(self, -1)
        self.fields[name][2].SetValidator(self.validator(self, name))
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
    
    def __init__(self, parent, getProfile, validator=None):
        wx.Panel.__init__(self, parent, -1)
        
        self.getProfile = getProfile
        self.validator = ConfigValidator if validator is None else validator
        self.fields = {}
        self.field_order = []

class ConfigValidator(wx.PyValidator):
    def __init__(self, panel, key):
        wx.PyValidator.__init__(self)
        self.key = key
        self.panel = panel

    Clone = lambda self: ConfigValidator(self.panel, self.key)

    def Validate(self, parent):
        return True

    def TransferToWindow(self):
        win = self.GetWindow()
        profile = self.panel.getProfile()
        data = pos.config['db.'+profile, self.key]
        
        win.Enable(self.panel.fields[self.key][0].IsChecked() or data is not None)
        self.panel.fields[self.key][0].SetValue(data is not None)
        win.SetValue(data if data is not None else '')
        return True

    def TransferFromWindow(self):
        win = self.GetWindow()
        profile = self.panel.getProfile()
        
        if not self.panel.fields[self.key][0].IsChecked():
            pos.config['db.'+profile, self.key] = None
        else:
            pos.config['db.'+profile, self.key] = win.GetValue()
        return True
