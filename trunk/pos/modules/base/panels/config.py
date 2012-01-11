import wx

import pos
import importlib

from pos.modules.base.panels import FormPanel
from pos.modules.base.objects import validator as base_validator
from pos.modules.base.objects.formatter import TextFormatter

class MainConfigPanel(wx.Panel):
    def _init_sizers(self):
        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        for btn in self.btns:
            self.controlSizer.Add(self.controls[btn], 0, border=10, flag=wx.RIGHT)

        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.AddSizer(self.controlSizer, 0)
        self.mainSizer.Add(self.listBook, 1, border=10, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(self.mainSizer)

    def _init_controls(self):
        btns = [('Edit', 'edit', self.OnEditButton),
                ('OK', 'save', self.OnSaveButton),
                ('Cancel', 'cancel', self.OnCancelButton)]
        
        self.controls = {}
        for b in btns:
            self.controls[b[0]] = wx.Button(self, -1, label=b[0])
            #self.controls[b[0]] = wx.BitmapButton(self, -1,
            #        bitmap=wx.Bitmap('./images/commands/'+b[1]+'.png', wx.BITMAP_TYPE_PNG),
            #        style=wx.BU_AUTODRAW)
            self.controls[b[0]].Bind(wx.EVT_BUTTON, b[2])
        self.btns = [b[0] for b in btns] 

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)
        
        self.editing = False
        
        self.listBook = wx.Listbook(self, -1)
        self.listBook.Bind(wx.EVT_LISTBOOK_PAGE_CHANGED, self.OnListbookPageChanged)
        
        self._init_controls()
        self._init_sizers()
        
        self.panels = []
        self.panel_names = []
        for mod in pos.modules.all_wrappers():
            panels = importlib.import_module('pos.modules.'+mod.name+'.panels')
            if panels is not None and hasattr(panels, 'ModuleConfigPanel'):
                panel = panels.ModuleConfigPanel(self.listBook)
                self.panels.append(panel)
                self.panel_names.append(mod.name)
                if hasattr(panel, 'label') and panel.label:
                    self.listBook.AddPage(panel, panel.label)
                else:
                    self.listBook.AddPage(panel, '[%s]' % (mod.name,))
                panel.TransferDataToWindow()
        
        self.enableEditing(False)

    def enableEditing(self, enable):
        self.editing = enable
        self.controls['Edit'].Enable(not enable)
        self.controls['OK'].Enable(enable)
        self.controls['Cancel'].Enable(enable)
        
        self.listBook.GetListView().Enable(not enable)
        name, panel = self.getSelectedPanel()
        panel.Enable(enable)

    def getSelectedPanel(self):
        selected = self.listBook.GetSelection()
        panel = self.listBook.GetPage(selected)
        name = self.panel_names[self.panels.index(panel)]
        return name, panel

    def saveChanges(self):
        name, panel = self.getSelectedPanel()
        if hasattr(panel, 'section'):
            pos.config[panel.section] = panel.data
        else:
            pos.config['mod.'+name] = panel.data
        pos.config.save()

    def OnListbookPageChanged(self, event):
        event.Skip()
        name, panel = self.getSelectedPanel()
        panel.Enable(self.editing)
    
    def OnEditButton(self, event):
        event.Skip()
        self.enableEditing(True)
    
    def OnSaveButton(self, event):
        event.Skip()
        name, panel = self.getSelectedPanel()
        if not panel.Validate():
            wx.MessageBox('The form contains some invalid fields.\nCannot save changes.', 'Error', wx.OK)
            return
        panel.TransferDataFromWindow()
        self.saveChanges()
        self.enableEditing(False)

    def OnCancelButton(self, event):
        event.Skip()
        name, panel = self.getSelectedPanel()
        panel.TransferDataToWindow()
        self.enableEditing(False)

class ModuleConfigPanel(FormPanel):
    label = 'Main'
    section = 'menu'
    
    def __init__(self, parent):
        FormPanel.__init__(self, parent, -1, DataValidator)
        
        self.createField('Show empty root items', wx.CheckBox, 'show_empty_root_items', pos.config['menu', 'show_empty_root_items'])
        self.createField('Show disabled items', wx.CheckBox, 'show_disabled_items', pos.config['menu', 'show_disabled_items'])
        #self.createField('Open in fullscreen', wx.CheckBox, 'fullscreen', pos.config['app', 'fullscreen'])
        self._init_fields()

class DataValidator(base_validator.BaseValidator):
    def GetWindowData(self):
        win = self.GetWindow()
        if self.key in ('show_empty_root_items', 'show_disabled_items'):
            return '1' if win.IsChecked() else ''
    
    def ValidateWindowData(self, data):
        return True
    
    def SetWindowData(self, data):
        win = self.GetWindow()
        if self.key in ('show_empty_root_items', 'show_disabled_items'):
            value = pos.config['menu', self.key]
            win.SetValue(bool(value))
