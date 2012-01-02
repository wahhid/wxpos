import wx
from wx.lib.scrolledpanel import ScrolledPanel

from pos.modules.base.objects import validator as base_validator

class FormPanel(ScrolledPanel):#wx.PyPanel):
    def _init_sizers(self):
        self.formSizer = wx.GridBagSizer(hgap=5, vgap=5)
        for row, name in enumerate(self.field_order):
            f = self.fields[name]
            if f['sep']:
                self.formSizer.Add(f['labelObj'], (row, 0), flag=wx.EXPAND | wx.ALL)
                self.formSizer.Add(f['fieldObj'], (row, 1), border=10, flag=wx.EXPAND | wx.ALL)
            else:
                #flag = (wx.EXPAND | wx.ALL) if f[2] else 0
                flag = 0
                self.formSizer.Add(f['labelObj'], (row, 0), flag=wx.EXPAND | wx.ALL)
                self.formSizer.Add(f['fieldObj'], (row, 1), flag=flag)
        self.formSizer.AddGrowableCol(1, 1)
        self.SetSizerAndFit(self.formSizer)

    def _init_fields(self):
        self._init_sizers()

        self.SetupScrolling()
        self.__data = self.data.copy()

    def __init__(self, parent, id, validator=None):
        #wx.PyPanel.__init__(self, parent, id, style=wx.TAB_TRAVERSAL | wx.WS_EX_VALIDATE_RECURSIVELY)
        ScrolledPanel.__init__(self, parent, id, style=wx.TAB_TRAVERSAL | wx.WS_EX_VALIDATE_RECURSIVELY)
        
        if validator is not None:
            self.validator = base_validator.validator(validator)
        else:
            self.validator = None
        
        self.fields = {}
        self.field_order = []
        self.data = {}

    def createField(self, label_text, wxObj, field_name, default_value, validator=None, formatter=None, **kwargs):
        self.field_order.append(field_name)
        self.data[field_name] = default_value
        
        validator_class = self.validator if validator is None else base_validator.validator(validator)
        if validator_class is not None:
            V = validator_class(panel=self, key=field_name, formatter=formatter)
        else:
            V = None
        
        self.fields[field_name] = {}
        if label_text is None:
            self.fields[field_name]['sep'] = True
            self.fields[field_name]['labelObj'] = wxObj(self, -1, **kwargs)
            self.fields[field_name]['fieldObj'] = wx.StaticLine(self, -1)
            if V is not None:
                self.fields[field_name]['labelObj'].SetValidator(V)
        else:
            self.fields[field_name]['sep'] = False
            self.fields[field_name]['labelObj'] = wx.StaticText(self, -1, label=label_text)
            self.fields[field_name]['fieldObj'] = wxObj(self, -1, **kwargs)
            if V is not None:
                self.fields[field_name]['fieldObj'].SetValidator(V)

    def getField(self, field_name):
        if self.fields[field_name]['sep']:
            return self.fields[field_name]['labelObj']
        else:
            return self.fields[field_name]['fieldObj']
    
    def resetForm(self):
        self.data = self.__data.copy()
        self.TransferDataToWindow()
    
    def fillForm(self, item=None, data=None):
        self.data = self.__data.copy()
        if item is not None:
            self.fillData(item)
        if data is not None:
            self.data.update(data)
        self.TransferDataToWindow()
    
    def fillData(self, item):
        if item is None: return
        item.fillDict(self.data)
