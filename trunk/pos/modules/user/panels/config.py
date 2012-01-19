import wx

import pos

class UserConfigPanel(wx.Panel):
    label = 'Users'
    
    def _init_sizers(self):
        self.mainSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.mainSizer.Add(self.allowEmptyLbl, 0)
        self.mainSizer.Add(self.allowEmptyCb, 0, border=10, flag=wx.LEFT)

        self.SetSizer(self.mainSizer)

    def _init_main(self):
        self.allowEmptyLbl = wx.StaticText(self, -1, label='Allow empty passwords')
        self.allowEmptyCb = wx.CheckBox(self, -1)
        self.allowEmptyCb.SetValidator(DataValidator(self, 'allow_empty_passwords'))
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)

        self._init_main()
        self._init_sizers()
        self.data = {}

class DataValidator(wx.PyValidator):
    def __init__(self, panel, key):
        wx.PyValidator.__init__(self)
        self.panel = panel
        self.key = key

    Clone = lambda self: DataValidator(self.panel, self.key)

    def Validate(self, parent):
        return True

    def TransferToWindow(self):
        win = self.GetWindow()
        if self.key == 'allow_empty_passwords':
            allow = pos.config['mod.user', 'allow_empty_passwords']
            win.SetValue(bool(allow))
        return True

    def TransferFromWindow(self):
        win = self.GetWindow()
        if self.key == 'allow_empty_passwords':
            data = '1' if win.IsChecked() else ''
        self.panel.data[self.key] = data
        return True
