import wx

from pos.modules.customer.windows.customerCatalogList import CustomerCatalogList
import pos.modules.customer.objects.customer as customer

import pos.modules.currency.objects.currency as currency

import pos.modules.sales.objects.ticket as ticket

from ..dialogs.payDialog import PayDialog

from pos.modules.base.objects.idManager import ids

class DebtsPanel(wx.Panel):
    def _init_sizers(self):
        self.formSizer = wx.GridBagSizer(hgap=0, vgap=0)
        self.formSizer.Add(self.customerLbl, (0, 0))
        self.formSizer.Add(self.customerTxt, (0, 1))
        self.formSizer.Add(self.currentDebtLbl, (1, 0))
        self.formSizer.Add(self.currentDebtTxt, (1, 1))
        self.formSizer.Add(self.maxDebtLbl, (2, 0))
        self.formSizer.Add(self.maxDebtTxt, (2, 1))
        self.formSizer.AddGrowableCol(1, 1)

        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlSizer.Add(self.payBtn, 0, flag=wx.ALIGN_RIGHT)
        
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.Add(self.customerList, 1, border=5, flag=wx.EXPAND | wx.ALL)
        self.mainSizer.AddSizer(self.formSizer, 1, border=5, flag=wx.EXPAND | wx.ALL)
        self.mainSizer.AddSizer(self.controlSizer, 0, border=5, flag=wx.EXPAND | wx.ALL)

        self.SetSizer(self.mainSizer)

    def _init_main(self):
        self.customerLbl = wx.StaticText(self, -1, label='Customer')
        self.customerTxt = wx.TextCtrl(self, -1, style=wx.TE_READONLY)

        self.currentDebtLbl = wx.StaticText(self, -1, label='Current Debt')
        self.currentDebtTxt = wx.TextCtrl(self, -1, style=wx.TE_READONLY)

        self.maxDebtLbl = wx.StaticText(self, -1, label='Max Debt')
        self.maxDebtTxt = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        
        self.customerList = CustomerCatalogList(self)
        self.customerList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnCustomerCatalogItemActivate)

        self.payBtn = wx.Button(self, -1, label='Pay')
        self.payBtn.Bind(wx.EVT_BUTTON, self.OnPayButton)
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)

        self.current_debt = 0

        self._init_main()
        self._init_sizers()

        self.payBtn.Enable(False)

    def OnCustomerCatalogItemActivate(self, event):
        event.Skip()
        selected = self.customerList.GetFirstSelected()
        c, image_id = self.customerList.getItem(selected)
        if c is not None and image_id == 1:
            self.customer = c
            self.current_debt = c.getDebt()
            self.customerTxt.SetValue(c.data['name'])
            self.currentDebtTxt.SetValue(currency.default.format(self.current_debt))
            max_debt = c.data['max_debt']
            if max_debt is None:
                self.maxDebtTxt.SetValue('')
            else:
                self.maxDebtTxt.SetValue(str(max_debt))
            self.payBtn.Enable(True)
        else:
            self.customer = None
            self.payBtn.Enable(False)

    def OnPayButton(self, event):
        event.Skip()
        dlg = PayDialog(None, self.current_debt, currency.default, None)
        ret = dlg.ShowModal()
        if ret == wx.ID_OK:
            tickets = ticket.find(list=True, customer=self.customer, payment_method='debt', date_paid=None)
            for t in tickets:
                t.pay(*dlg.payment)
