import wx

from pos.modules.base.objects.idManager import ids

VIEW_MODE, EDIT_MODE = 0, 1

class ManagePanel:
    def _init_sizers(self):
        self.sideSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sideSizer.Add(self.itemsLbl, 0, border=0, flag=wx.BOTTOM)
        self.sideSizer.Add(self.itemList, 1, border=0, flag=wx.ALL | wx.EXPAND)

        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        for btn in self.btns:
            self.controlSizer.Add(self.controls[btn], 0, border=10, flag=wx.RIGHT)
        
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
        self.formPanel.SetSizer(self.formSizer)

        self.panelSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.panelSizer.AddSizer(self.controlSizer, 0)
        self.panelSizer.Add(self.formPanel, 1, border=10, flag=wx.EXPAND | wx.ALL)

        self.mainSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.mainSizer.AddSizer(self.sideSizer, 1, border=10, flag=wx.EXPAND | wx.ALL)
        self.mainSizer.AddSizer(self.panelSizer, 3, border=10, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(self.mainSizer)

    def _init_controls(self):
        btns = [('New', 'add', self.OnNewButton),
                ('Edit', 'edit', self.OnEditButton),
                ('Delete', 'delete', self.OnDeleteButton),
                ('Save', 'save', self.OnSaveButton),
                ('Cancel', 'cancel', self.OnCancelButton)]
        
        self.controls = {}
        for b in btns:
            #self.controls[b[0]] = wx.Button(self, -1, label=b[0])
            self.controls[b[0]] = wx.BitmapButton(self, -1,
                    bitmap=wx.Bitmap('./images/commands/'+b[1]+'.png', wx.BITMAP_TYPE_PNG),
                    style=wx.BU_AUTODRAW)
            self.controls[b[0]].Bind(wx.EVT_BUTTON, b[2])
        self.btns = map(lambda b: b[0], btns)
    
    def _init_panel(self, label, validator):
        self.itemsLbl = wx.StaticText(self, -1, label=label)
        self.itemList = wx.ListCtrl(self, -1, style=wx.LC_LIST)
        self.itemList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
        
        self.validator = validator
        self.formPanel = wx.Panel(self, -1,
                    style=wx.TAB_TRAVERSAL | wx.WS_EX_VALIDATE_RECURSIVELY)
        
        self.fields = {}
        self.field_order = []
        self.data = {}
        
        self._init_controls()

    def _init_fields(self):
        self._init_sizers()

        self.__data = self.data.copy()

        self.viewItem()
        self.updateItemList()

    def createField(self, label_text, wxObj, field_name, default_value, **kwargs):
        self.field_order.append(field_name)
        self.fields[field_name] = {}
        if label_text is None:
            self.fields[field_name]['sep'] = True
            self.fields[field_name]['labelObj'] = wxObj(self.formPanel, -1, **kwargs)
            self.fields[field_name]['fieldObj'] = wx.StaticLine(self.formPanel, -1)
            self.fields[field_name]['labelObj'].SetValidator(self.validator(self, field_name))
        else:
            self.fields[field_name]['sep'] = False
            self.fields[field_name]['labelObj'] = wx.StaticText(self.formPanel, -1, label=label_text)
            self.fields[field_name]['fieldObj'] = wxObj(self.formPanel, -1, **kwargs)
            self.fields[field_name]['fieldObj'].SetValidator(self.validator(self, field_name))
        self.data[field_name] = default_value

    def getField(self, field_name):
        if self.fields[field_name]['sep']:
            return self.fields[field_name]['labelObj']
        else:
            return self.fields[field_name]['fieldObj']

    def setMode(self, mode):
        self.mode = mode
        i = self.getCurrentItem()
        if mode == EDIT_MODE:
            enable_list = False
            enabled_controls = ('Save', 'Cancel')
            enable_form = True
        elif mode == VIEW_MODE:
            enable_list = True
            enabled_controls = ['New']+(['Edit', 'Delete'] if i is not None else [])
            if 'Edit' in enabled_controls and not self.canEditItem(i):
                enabled_controls.remove('Edit')
            if 'Delete' in enabled_controls and not self.canDeleteItem(i):
                enabled_controls.remove('Delete')
            enable_form = False
        
        self.itemList.Enable(enable_list)
        for btn in self.btns:
            self.controls[btn].Enable(btn in enabled_controls)
        for name in self.fields.keys():
            self.getField(name).Enable(enable_form)
    
    def updateItemList(self):
        items = self.getItems()
        self.itemList.ClearAll()
        for i in items:
            item = wx.ListItem()
            item.SetText(i['text'])
            self.itemList.InsertItem(item)

    def getCurrentItem(self):
        index = self.itemList.GetFirstSelected()
        if index == -1:
            return None
        else:
            item = self.itemList.GetItem(index)
            return self.getItem(item)

    def viewItem(self):
        self.setMode(VIEW_MODE)
        self.clearForm()
        self.fillForm()

    def editItem(self):
        self.setMode(EDIT_MODE)
        self.clearForm()
        self.fillForm()

    def fillForm(self):
        self.fillData()
        self.formPanel.TransferDataToWindow()

    def clearForm(self):
        self.data = self.__data.copy()
        self.formPanel.TransferDataToWindow()

    def saveItem(self):
        item = self.getCurrentItem()
        if item is None:
            newitem = self.newItem()
            if newitem is None:
                wx.MessageBox('An error occured while adding the new item', 'Error',
                              wx.OK)
                return False
            else:
                return True
        else:
            update = self.updateItem(item)
            if not update:
                wx.MessageBox('An error occured while updating the item', 'Error',
                              wx.OK)
                return False
            else:
                return True
    
    def OnListItemSelected(self, event):
        event.Skip()
        self.viewItem()

    def OnNewButton(self, event):
        event.Skip()
        self.clearForm()
        for i in range(self.itemList.GetItemCount()):
            self.itemList.Select(i, 0)
        self.editItem()

    def OnEditButton(self, event):
        event.Skip()
        i = self.getCurrentItem()
        if i is None:
            return
        if not self.canEditItem(i):
            return
        self.editItem()

    def OnDeleteButton(self, event):
        event.Skip()
        i = self.getCurrentItem()
        if i is None:
            return
        if not self.canDeleteItem(i):
            return
        doDelete = wx.MessageBox('Are you sure you want to delete this item?\nThis cannot be undone.', 'Delete item',
                                wx.OK | wx.CANCEL | wx.ICON_WARNING)
        if doDelete == wx.OK:
            if not i.delete():
                wx.MessageBox('An error occured while deleting item', 'Error', wx.OK)
            else:
                self.updateItemList()
                self.viewItem()
    
    def OnSaveButton(self, event):
        event.Skip()
        if not self.formPanel.Validate():
            wx.MessageBox('The form contains some invalid fields.\nCannot save item.', 'Error', wx.OK)
            return
        self.formPanel.TransferDataFromWindow()
        if self.saveItem():
            self.updateItemList()
            self.viewItem()

    def OnCancelButton(self, event):
        event.Skip()
        self.viewItem()

    #########################
    ###  PANEL  SPECIFIC  ###
    #########################
    def getItems(self):
        return []

    def getItem(self, item):
        return None

    def canEditItem(self, item):
        return True

    def canDeleteItem(self, item):
        return True

    def newItem(self):
        return False

    def updateItem(self, item):
        return False

    def fillData(self):
        pass
