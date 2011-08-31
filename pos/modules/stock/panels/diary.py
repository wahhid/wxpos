import wx

from pos.modules.base.objects.idManager import ids

import pos.modules.currency.objects.currency as currency

import pos.modules.stock.objects.product as product
import pos.modules.stock.objects.category as category

from pos.modules.stock.windows.productCatalogList import ProductCatalogList

class StockDiaryPanel(wx.Panel):
    def _init_sizers(self):
        self.formSizer = wx.GridBagSizer(hgap=10, vgap=10)

        self.formSizer.Add(self.catalogList, (0, 0), (1, 2), flag=wx.EXPAND | wx.ALL)
        
        self.formSizer.Add(self.operationBox, (1, 0), (1, 2))
        
        self.formSizer.Add(self.quantityLbl, (2, 0), flag=wx.EXPAND | wx.ALL)
        self.formSizer.Add(self.quantitySpin, (2, 1))

        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlSizer.Add(self.editBtn, 0, border=10, flag=wx.RIGHT)
        self.controlSizer.Add(self.saveBtn, 0, border=10, flag=wx.RIGHT)
        self.controlSizer.Add(self.cancelBtn, 0, border=10, flag=wx.RIGHT)

        self.formSizer.AddSizer(self.controlSizer, (3, 0), (1, 2),
                                flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER)

        self.formSizer.AddGrowableRow(0, 1)
        self.formSizer.AddGrowableCol(1, 1)
        
        self.SetSizer(self.formSizer)
    
    def __init__(self, parent):
        wx.Panel.__init__(self, id=ids['stockDiaryPanel'], parent=parent, style=wx.TAB_TRAVERSAL)
        
        self.catalogList = ProductCatalogList(self, show_only_in_stock=True)
        self.catalogList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnCatalogItemSelect)
        self.catalogList.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnCatalogItemDeselect)
        self.catalogList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnCatalogItemActivate)

        box_choices = ['In', 'Modification']
        self.operationBox = wx.RadioBox(self, -1, label="Operation", choices=box_choices)

        self.quantityLbl = wx.StaticText(self, -1, label='Quantity')
        self.quantitySpin = wx.SpinCtrl(self, -1, value='0', style=wx.SP_ARROW_KEYS, min=0)

        self.editBtn = wx.Button(self, -1, label='Edit')
        self.editBtn.Bind(wx.EVT_BUTTON, self.OnEditButton)

        self.saveBtn = wx.Button(self, -1, label='Save')
        self.saveBtn.Bind(wx.EVT_BUTTON, self.OnSaveButton)

        self.cancelBtn = wx.Button(self, -1, label='Cancel')
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancelButton)

        self._init_sizers()


        self.product = None
        self.enableForm(False)

    def canEdit(self):
        if self.product is None:
            return False
        else:
            quantity = self.product.data['quantity']
            if quantity is None:
                return False
            else:
                return True

    def enableForm(self, en):
        self.catalogList.Enable(not en)
        self.operationBox.Enable(en)
        self.quantitySpin.Enable(en)
        self.saveBtn.Enable(en)
        self.cancelBtn.Enable(en)

        if self.canEdit() and not en:
            quantity = self.product.data['quantity']
            self.editBtn.Enable(True)
            self.quantitySpin.SetValue(quantity)
        elif en:
            self.editBtn.Enable(False)
        else:
            self.editBtn.Enable(False)
            self.quantitySpin.SetValue(0)

    def saveChanges(self):
        quantity = self.quantitySpin.GetValue()
        operation = 'in' if self.operationBox.GetSelection() == 0 else 'edit'
        success = self.product.updateQuantity(quantity, operation)
        if not success:
            wx.MessageBox('An error occured while saving changes.', 'Error',
                          wx.OK | wx.ICON_ERROR)
            return False
        else:
            return True

    def OnEditButton(self, event):
        event.Skip()
        if self.canEdit():
            self.enableForm(True)
    
    def OnSaveButton(self, event):
        event.Skip()
        if self.saveChanges():
            self.enableForm(False)

    def OnCancelButton(self, event):
        event.Skip()
        self.enableForm(False)

    def OnCatalogItemDeselect(self, event):
        event.Skip()
        self.product = None
        self.enableForm(False)

    def OnCatalogItemSelect(self, event):
        event.Skip()
        selected = self.catalogList.GetFirstSelected()
        p, image_id = self.catalogList.getItem(selected)
        if p is not None and image_id == 1:
            self.product = p
        else:
            self.product = None
        self.enableForm(False)

    def OnCatalogItemActivate(self, event):
        event.Skip()
        if self.canEdit():
            self.enableForm(True)
