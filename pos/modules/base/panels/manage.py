import wx

import pos

from .form import FormPanel

VIEW_MODE, EDIT_MODE = 0, 1

class ManagePanel(wx.PyPanel):
    def _init_sizers(self):
        self.sideSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sideSizer.Add(self.itemsLbl, 0, border=0, flag=wx.BOTTOM)
        self.sideSizer.Add(self.itemList, 1, border=0, flag=wx.ALL | wx.EXPAND)

        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        for btn in self.btns:
            self.controlSizer.Add(self.controls[btn], 0, border=10, flag=wx.RIGHT)

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
                    bitmap=wx.Bitmap('./res/base/images/'+b[1]+'.png', wx.BITMAP_TYPE_PNG),
                    style=wx.BU_AUTODRAW)
            self.controls[b[0]].Bind(wx.EVT_BUTTON, b[2])
        self.btns = map(lambda b: b[0], btns)

    def _init_fields(self):
        self.formPanel._init_fields()
        self._init_sizers()

        self.updateItemList()
    
    def __init__(self, parent, id, label, obj, validator):
        wx.PyPanel.__init__(self, parent, id)
        
        self.itemsLbl = wx.StaticText(self, -1, label=label)
        self.itemList = wx.ListCtrl(self, -1, style=wx.LC_LIST | wx.LC_SORT_ASCENDING)
        self.itemList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
        
        self.formPanel = FormPanel(self, -1, validator)

        self.object = obj
        self.items = {}
        
        self._init_controls()

    def createField(self, label_text, wxObj, field_name, default_value, validator=None, formatter=None, **kwargs):
        self.formPanel.createField(label_text, wxObj, field_name, default_value, validator, formatter, **kwargs)

    def getField(self, field_name):
        return self.formPanel.getField(field_name)
    
    def updateItemList(self):
        self.items = {}
        items = self.getItems()
        self.itemList.ClearAll()
        _index = 0
        for i in items:
            item = wx.ListItem()
            item.SetText(i[1])
            item.SetData(_index)
            self.itemList.InsertItem(item)
            self.items[_index] = i[0]
            _index += 1
        
        self.formPanel.resetForm()
        self.viewItem()

    def getCurrentItem(self):
        index = self.itemList.GetFirstSelected()
        if index == -1:
            return None
        else:
            return self.items[self.itemList.GetItemData(index)]

    def viewItem(self):
        self.itemList.Enable(True)
        
        item = self.getCurrentItem()
        enabled_controls = ['New']
        if item is not None and self.canEditItem(item):
            enabled_controls.append('Edit')
        if item is not None and self.canDeleteItem(item):
            enabled_controls.append('Delete')
        for btn in self.btns:
            self.controls[btn].Enable(btn in enabled_controls)
        
        self.formPanel.Enable(False)
        self.fillForm()

    def editItem(self):
        self.itemList.Enable(False)
        
        enabled_controls = ('Save', 'Cancel')
        for btn in self.btns:
            self.controls[btn].Enable(btn in enabled_controls)
        
        self.formPanel.Enable(True)
        self.fillForm()

    def fillForm(self):
        item = self.getCurrentItem()
        self.formPanel.fillForm(item=item, data=None)
    
    def saveItem(self):
        item = self.getCurrentItem()
        if item is None:
            newitem = self.newItem()
            if not newitem:
                wx.MessageBox('An error occured while adding the new item', 'Error',
                              wx.OK)
                return False
        else:
            update = self.updateItem(item)
            if not update:
                wx.MessageBox('An error occured while updating the item', 'Error',
                              wx.OK)
                return False
        return True
    
    def OnListItemSelected(self, event):
        event.Skip()
        self.viewItem()

    def OnNewButton(self, event):
        event.Skip()
        self.formPanel.resetForm()
        for i in range(self.itemList.GetItemCount()):
            self.itemList.Select(i, 0)
        self.editItem()

    def OnEditButton(self, event):
        event.Skip()
        i = self.getCurrentItem()
        if i is not None and self.canEditItem(i):
            self.editItem()

    def OnDeleteButton(self, event):
        event.Skip()
        i = self.getCurrentItem()
        if i is not None and self.canDeleteItem(i):
            doDelete = wx.MessageBox('Are you sure you want to delete this item?\nThis cannot be undone.', 'Delete item',
                                    wx.OK | wx.CANCEL | wx.ICON_WARNING)
            if doDelete == wx.OK:
                if not i.delete():
                    wx.MessageBox('An error occured while deleting item', 'Error', wx.OK)
                else:
                    self.updateItemList()
    
    def OnSaveButton(self, event):
        event.Skip()
        if not self.formPanel.Validate():
            wx.MessageBox('The form contains some invalid fields.\nCannot save item.', 'Error', wx.OK)
            return
        self.formPanel.TransferDataFromWindow()
        if self.saveItem():
            self.updateItemList()

    def OnCancelButton(self, event):
        event.Skip()
        self.formPanel.resetForm()
        self.viewItem()

    def canEditItem(self, item):
        return True

    def canDeleteItem(self, item):
        return True
    
    def getItems(self):
        session = pos.database.session()
        return session.query(self.object, self.object.display).all()

    def newItem(self):
        item = self.object()
        return self.updateItem(item)

    def updateItem(self, item):
        item.update(**self.formPanel.data)
        return True
