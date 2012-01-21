import wx
import os
import zipfile

import pos

class ModulesPanel(wx.Panel):
    def _init_sizers(self):
        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlSizer.Add(self.exportBtn, 0, border=5, flag=wx.RIGHT | wx.LEFT)
        self.controlSizer.Add(self.enableBtn, 0, border=5, flag=wx.RIGHT | wx.LEFT)
        self.controlSizer.Add(self.disableBtn, 0, border=5, flag=wx.RIGHT | wx.LEFT)
        
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.Add(self.modulesList, 1, border=10, flag=wx.EXPAND | wx.ALL)
        self.mainSizer.Add(self.controlSizer, 0, border=10, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(self.mainSizer)

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)
        
        self.modulesList = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.modulesList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnModuleItemSelected)
        self.modulesList.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnModuleItemDeselected)
        self.modulesList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnModuleItemActivated)
        
        self.exportBtn = wx.Button(self, -1, 'Export...')
        self.exportBtn.Enable(False)
        self.exportBtn.Bind(wx.EVT_BUTTON, self.OnExportButton)
        
        self.disableBtn = wx.Button(self, -1, 'Disable')
        self.disableBtn.Enable(False)
        self.disableBtn.Bind(wx.EVT_BUTTON, self.OnDisableButton)
        
        self.enableBtn = wx.Button(self, -1, 'Enable')
        self.enableBtn.Enable(False)
        self.enableBtn.Bind(wx.EVT_BUTTON, self.OnEnableButton)
        
        disabled_str = pos.config['mod', 'disabled_modules']
        self.disabled = disabled_str.split(',') if disabled_str != '' else []
        self.headers = ['Module', 'Name', 'Dependencies', 'Enabled']
        
        for col, text in enumerate(self.headers):
            self.modulesList.InsertColumn(col, text)
        
        self.fillList()
        
        self._init_sizers()
    
    def fillList(self, update=False):
        self.modules_dict = dict([(mod.name, mod) for mod in pos.modules.all_wrappers()])
        rows = [('['+mod.name+']' if mod.disabled else mod.name, mod.loader.name if mod.loader else 'None', ', '.join(mod.loader.dependencies) if mod.loader else 'None', str(mod.name not in self.disabled)) for mod in self.modules_dict.itervalues()]
        if update:
            for index, item in enumerate(rows):
                for col, text in enumerate(item):
                    self.modulesList.SetStringItem(index, col, text)
        else:
            self.modulesList.DeleteAllItems()
            last = len(rows)+1
            for item in rows:
                index = self.modulesList.InsertStringItem(last, item[0])
                for col, text in enumerate(item[1:]):
                    self.modulesList.SetStringItem(index, col+1, text)
            
            for i in range(len(self.headers)):
                self.modulesList.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
    
    def getSelectedModules(self):
        selected = self.modulesList.GetFirstSelected()
        selected_indices = []
        while selected != -1:
            selected_indices.append(selected)
            selected = self.modulesList.GetNextSelected(selected)
        
        return selected_indices
    
    def _enableModules(self, items, enable=None):
        if enable is None:
            for item in items:
                name = self.modulesList.GetItemText(item, 0)
                if name.startswith('['): name = name[1:-1]
                if name in self.disabled:
                    self.disabled.remove(name)
                else:
                    self.disabled.append(name)
        elif enable:
            for item in items:
                name = self.modulesList.GetItemText(item, 0)
                if name.startswith('['): name = name[1:-1]
                try:
                    self.disabled.remove(name)
                except ValueError:
                    pass
        else:
            for item in items:
                name = self.modulesList.GetItemText(item, 0)
                if name.startswith('['): name = name[1:-1]
                if name not in self.disabled:
                    self.disabled.append(name)
        
        pos.config['mod', 'disabled_modules'] = ','.join(self.disabled)
        pos.config.save()
        
        self.fillList(update=True)
    
    def OnModuleItemDeselected(self, event):
        event.Skip()
        selected_indices = self.getSelectedModules()
        self.exportBtn.Enable(len(selected_indices)>0)
        self.enableBtn.Enable(len(selected_indices)>0)
        self.disableBtn.Enable(len(selected_indices)>0)
    
    def OnModuleItemSelected(self, event):
        event.Skip()
        selected_indices = self.getSelectedModules()
        self.exportBtn.Enable(len(selected_indices)>0)
        self.enableBtn.Enable(len(selected_indices)>0)
        self.disableBtn.Enable(len(selected_indices)>0)
    
    def OnModuleItemActivated(self, event):
        event.Skip()
        selected_indices = self.getSelectedModules()
        self._enableModules(selected_indices, None)

    def OnExportButton(self, event):
        event.Skip()
        selected_indices = self.getSelectedModules()
        
        wildcard = "Zip file (*.zip)|*.zip|All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Choose a zip file", os.getcwd(), "", wildcard, wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            target = dialog.GetPath()

            z = zipfile.PyZipFile(target, 'w')
            for item in selected_indices:
                name = self.modulesList.GetItemText(item, 0)
                z.writepy('pos/modules/'+name, 'pos/modules')
            z.close()

    def OnEnableButton(self, event):
        event.Skip()
        selected_indices = self.getSelectedModules()
        self._enableModules(selected_indices, True)

    def OnDisableButton(self, event):
        event.Skip()
        selected_indices = self.getSelectedModules()
        self._enableModules(selected_indices, False)
