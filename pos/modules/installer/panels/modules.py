import wx

import os

import pos

from pos.modules.installer import utils

class ModulesPanel(wx.Panel):
    def _init_sizers(self):
        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlSizer.Add(self.exportBtn, 0, border=5, flag=wx.RIGHT | wx.LEFT)
        self.controlSizer.Add(self.enableBtn, 0, border=5, flag=wx.RIGHT | wx.LEFT)
        self.controlSizer.Add(self.disableBtn, 0, border=5, flag=wx.RIGHT | wx.LEFT)
        self.controlSizer.Add(self.installBtn, 0, border=5, flag=wx.RIGHT | wx.LEFT)
        self.controlSizer.Add(self.uninstallBtn, 0, border=5, flag=wx.RIGHT | wx.LEFT)
        
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
        
        self.enableBtn = wx.Button(self, -1, 'Enable')
        self.enableBtn.Enable(False)
        self.enableBtn.Bind(wx.EVT_BUTTON, self.OnEnableButton)
        
        self.disableBtn = wx.Button(self, -1, 'Disable')
        self.disableBtn.Enable(False)
        self.disableBtn.Bind(wx.EVT_BUTTON, self.OnDisableButton)
        
        self.installBtn = wx.Button(self, -1, 'Install...')
        self.installBtn.Bind(wx.EVT_BUTTON, self.OnInstallButton)
        
        self.uninstallBtn = wx.Button(self, -1, 'Uninstall')
        self.uninstallBtn.Enable(False)
        self.uninstallBtn.Bind(wx.EVT_BUTTON, self.OnUninstallButton)
        
        self.headers = ['Module', 'Name', 'Dependencies', 'Enabled']
        
        for col, text in enumerate(self.headers):
            self.modulesList.InsertColumn(col, text)
        
        self.fillList()
        
        self._init_sizers()
    
    def fillList(self, update=False):
        disabled_str = pos.config['mod', 'disabled_modules']
        disabled = disabled_str.split(',') if disabled_str != '' else []
        
        self.modules_dict = dict([(mod.name, mod) for mod in pos.modules.all_wrappers()])
        rows = [('['+mod.name+']' if mod.disabled else mod.name, mod.loader.name if mod.loader else 'None', ', '.join(mod.loader.dependencies) if mod.loader else 'None', str(mod.name not in disabled)) for mod in self.modules_dict.itervalues()]
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
        def get_name(item):
            name = self.modulesList.GetItemText(item, 0)
            return name[1:-1] if name.startswith('[') else name
        mod_names = [get_name(item) for item in items]
        
        utils.enableModule(mod_names, enable)
        
        self.fillList(update=True)
    
    def OnModuleItemDeselected(self, event):
        event.Skip()
        selected_indices = self.getSelectedModules()
        self.exportBtn.Enable(len(selected_indices) == 1)
        self.enableBtn.Enable(len(selected_indices)>0)
        self.disableBtn.Enable(len(selected_indices)>0)
        self.uninstallBtn.Enable(len(selected_indices)>0)
    
    def OnModuleItemSelected(self, event):
        event.Skip()
        selected_indices = self.getSelectedModules()
        self.exportBtn.Enable(len(selected_indices) == 1)
        self.enableBtn.Enable(len(selected_indices)>0)
        self.disableBtn.Enable(len(selected_indices)>0)
        self.uninstallBtn.Enable(len(selected_indices)>0)
    
    def OnModuleItemActivated(self, event):
        event.Skip()
        selected_indices = self.getSelectedModules()
        self._enableModules(selected_indices, None)

    def OnExportButton(self, event):
        event.Skip()
        selected_indices = self.getSelectedModules()
        
        wildcard = "Zip file (*.zip)|*.zip|All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Select the destination installer", os.getcwd(), "", wildcard, wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            target = dialog.GetPath()
            name = self.modulesList.GetItemText(selected_indices[0], 0)
            if name.startswith('['): name = name[1:-1]

            retCode = wx.MessageBox('Export source also for %s?' % (name,), 'Export module', style=wx.YES_NO | wx.ICON_QUESTION)
            export_source = (retCode == wx.YES)

            mod = self.modules_dict[name]
            utils.exportModule(mod, target, export_source=export_source)
    
    def OnInstallButton(self, event):
        event.Skip()
        
        wildcard = "Zip file (*.zip)|*.zip|All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Select the installer", os.getcwd(), "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            target = dialog.GetPath()
            info = utils.getInstallerInfo(target)
            
            if not info:
                wx.MessageBox('Invalid module installer.', 'Install module', style=wx.OK | wx.ICON_INFORMATION)
                return
            else:
                base_name, name, version = info
            
            retCode = wx.MessageBox('Install %s version %s?\n%s' % (base_name, version, name), 'Install module', style=wx.YES_NO | wx.ICON_QUESTION)
            if retCode != wx.YES:
                return
 
            if pos.modules.isInstalled(base_name):
                retCode = wx.MessageBox('%s is already installed. Do you want to replace it?' % (base_name,), 'Install module', style=wx.YES_NO | wx.ICON_QUESTION)
                replace = (retCode == wx.YES)
                utils.installModule(target, replace)
            else:
                utils.installModule(target, False)
    
    def OnUninstallButton(self, event):
        event.Skip()
        
        selected_indices = self.getSelectedModules()
        retCode = wx.MessageBox('Uninstall %d selected module(s)? This cannot be undone.' % (len(selected_indices)), 'Uninstall module', style=wx.YES_NO | wx.ICON_QUESTION)
        if retCode != wx.YES:
            return
        
        retCode = wx.MessageBox('Remove resources also? This cannot be undone.', 'Uninstall module', style=wx.YES_NO | wx.ICON_QUESTION)
        remove_res = (retCode == wx.YES)
        
        for item in selected_indices:
            name = self.modulesList.GetItemText(item, 0)
            if name.startswith('['): name = name[1:-1]
            utils.uninstallModule(name, remove_res)

    def OnEnableButton(self, event):
        event.Skip()
        selected_indices = self.getSelectedModules()
        self._enableModules(selected_indices, True)

    def OnDisableButton(self, event):
        event.Skip()
        selected_indices = self.getSelectedModules()
        self._enableModules(selected_indices, False)
