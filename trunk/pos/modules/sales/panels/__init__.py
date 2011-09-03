import wx

import pos.modules.user.objects.user as user

import pos.modules.customer.objects.customer as customer

import pos.modules.stock.objects.category as category
import pos.modules.stock.objects.product as product

import pos.modules.sales.objects.ticket as ticket
import pos.modules.sales.objects.ticketline as ticketline

from ..dialogs.editDialog import EditDialog
from ..dialogs.payDialog import PayDialog

from ..windows.ticketChoice import TicketChoice
from ..windows.ticketList import TicketList
from ..windows.catalogBook import CatalogBook

from pos.modules.base.objects.idManager import ids

class SalesPanel(wx.Panel):
    def _init_sizers(self):
        self.findSizer = wx.GridBagSizer(hgap=0, vgap=0)
        self.findSizer.Add(self.codeLbl, (0, 0))
        self.findSizer.Add(self.codeTxt, (0, 1))
        self.findSizer.Add(self.customerLbl, (1, 0))
        self.findSizer.Add(self.customerTxt, (1, 1))
        self.findSizer.Add(self.totalLbl, (2, 0))
        self.findSizer.Add(self.totalTxt, (2, 1))
        self.findSizer.AddGrowableCol(1, 1)

        self.tlActionSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.tlActionSizer.Add(self.newTicketlineBtn, 0, border=3, flag=wx.ALL | wx.EXPAND)
        self.tlActionSizer.Add(self.editBtn, 0, border=3, flag=wx.ALL | wx.EXPAND)
        self.tlActionSizer.Add(self.plusBtn, 0, border=3, flag=wx.ALL | wx.EXPAND)
        self.tlActionSizer.Add(self.minusBtn, 0, border=3, flag=wx.ALL | wx.EXPAND)

        self.tActionSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.tActionSizer.Add(self.newBtn, 0, border=3, flag=wx.ALL | wx.EXPAND)
        self.tActionSizer.Add(self.ticketChoice, 0, border=3, flag=wx.ALL | wx.EXPAND)
        self.tActionSizer.Add(self.closeBtn, 0, border=3, flag=wx.ALL | wx.EXPAND)
        self.tActionSizer.Add(self.cancelBtn, 0, border=3, flag=wx.ALL | wx.EXPAND)

        self.mainSizer = wx.GridBagSizer(hgap=0, vgap=0)
        self.mainSizer.AddSizer(self.tlActionSizer, (1, 0), (1, 1))
        self.mainSizer.AddSizer(self.tActionSizer, (0, 1), (1, 1))
        self.mainSizer.Add(self.ticketList, (1, 1), (1, 1), flag=wx.EXPAND | wx.ALL)
        self.mainSizer.AddSizer(self.findSizer, (1, 2), flag=wx.ALIGN_BOTTOM)
        self.mainSizer.Add(self.catalogBook, (2, 0), (1, 3), border=3, flag=wx.EXPAND | wx.ALL)

        #############################
        # T # TICKET ACTIONS        #
        # L #########################
        #   # TICKET LIST           #
        # A #  -------------------- #
        # C #  -------------------- #
        # T #  -------------------- #
        #############################
        # CATALOG BOOK              #
        #                           #
        #                           #
        #############################
        
        self.mainSizer.AddGrowableCol(1, 1)
        self.mainSizer.AddGrowableRow(1, 1)
        self.mainSizer.AddGrowableRow(2, 2)

        self.SetSizer(self.mainSizer)

    def _init_main(self):
        ### Ticket actions ###
        self.newBtn = wx.BitmapButton(self, -1,
                    bitmap=wx.Bitmap('./images/commands/add.png', wx.BITMAP_TYPE_PNG),
                    style=wx.BU_AUTODRAW)
        self.newBtn.Bind(wx.EVT_BUTTON, self.OnNewButton)

        self.ticketChoice = TicketChoice(self)
        self.ticketChoice.Bind(wx.EVT_CHOICE, self.OnTicketChoice)

        self.closeBtn = wx.BitmapButton(self, -1,
                    bitmap=wx.Bitmap('./images/commands/load.png', wx.BITMAP_TYPE_PNG),
                    style=wx.BU_AUTODRAW)
        self.closeBtn.Bind(wx.EVT_BUTTON, self.OnCloseButton)

        self.cancelBtn = wx.BitmapButton(self, -1,
                    bitmap=wx.Bitmap('./images/commands/cancel.png', wx.BITMAP_TYPE_PNG),
                    style=wx.BU_AUTODRAW)
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancelButton)

        ### Ticket list ###
        self.ticketList = TicketList(self)
        self.ticketList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnTicketlineItemActivate)
        self.ticketList.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnTicketlineItemRightClick)
        self.ticketList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnTicketlineItemSelect)
        self.ticketList.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnTicketlineItemDeselect)
        
        ### Ticketline actions ###
        self.newTicketlineBtn = wx.BitmapButton(self, -1,
                    bitmap=wx.Bitmap('./images/commands/add.png', wx.BITMAP_TYPE_PNG),
                    style=wx.BU_AUTODRAW)
        self.newTicketlineBtn.Bind(wx.EVT_BUTTON, self.OnNewTicketlineButton)
        
        self.editBtn = wx.BitmapButton(self, -1,
                    bitmap=wx.Bitmap('./images/commands/edit.png', wx.BITMAP_TYPE_PNG),
                    style=wx.BU_AUTODRAW)
        self.editBtn.Bind(wx.EVT_BUTTON, self.OnEditButton)

        self.plusBtn = wx.BitmapButton(self, -1,
                    bitmap=wx.Bitmap('./images/plus.png', wx.BITMAP_TYPE_PNG),
                    style=wx.BU_AUTODRAW)
        self.plusBtn.Bind(wx.EVT_BUTTON, self.OnPlusButton)
        
        self.minusBtn = wx.BitmapButton(self, -1,
                    bitmap=wx.Bitmap('./images/minus.png', wx.BITMAP_TYPE_PNG),
                    style=wx.BU_AUTODRAW)
        self.minusBtn.Bind(wx.EVT_BUTTON, self.OnMinusButton)

        ### Find Product ###
        self.codeLbl = wx.StaticText(self, -1, label='Barcode:')
        self.codeTxt = wx.TextCtrl(self, -1, style=wx.TE_PROCESS_ENTER)
        self.codeTxt.Bind(wx.EVT_TEXT_ENTER, self.OnCodeEnter)

        self.customerLbl = wx.StaticText(self, -1, label='Customer:')
        self.customerTxt = wx.TextCtrl(self, -1, style=wx.TE_READONLY)

        self.totalLbl = wx.StaticText(self, -1, label='Total:')
        self.totalTxt = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        
        #self.findBtn = wx.BitmapButton(self, -1,
        #            bitmap=wx.Bitmap('./images/commands/search.png', wx.BITMAP_TYPE_PNG),
        #            style=wx.BU_AUTODRAW)
        #self.findBtn.Bind(wx.EVT_BUTTON, self.OnFindButton)

        ### Catalog ###
        self.catalogBook = CatalogBook(self)
        self.catalogBook.productList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnProductCatalogItemActivate)
        self.catalogBook.customerList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnCustomerCatalogItemActivate)
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, ids['salesPanel'],
                style=wx.TAB_TRAVERSAL)

        # Accelerator Table: Press F3 to set focus to barcode field
        accTable = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_F3, ids['F3Command'])])
        self.Bind(wx.EVT_MENU, self.OnF3Command, id=ids['F3Command']) 
        self.SetAcceleratorTable(accTable)

        self._init_main()
        self._init_sizers()

        self.enableTicketActions(False)
        self.enableTicketlineActions(False)

        self.ticketChoice.updateList()

    ### Ticket list ###
    def setCurrentTicket(self, t):
        if t is None:
            self.ticketChoice.updateList()
            self.ticketList.clearLines()
            self.customerTxt.SetValue('')
            self.totalTxt.SetValue('')
            self.enableTicketActions(False)
            self.enableTicketlineActions(False)
        else:
            self.ticketChoice.setCurrentTicket(t)
            self.ticketList.updateList(t)
            c = t.data['customer']
            if c is None:
                self.customerTxt.SetValue('[None]')
            else:
                self.customerTxt.SetValue(c.data['name'])
            total = self.ticketList.getTotal()
            self.totalTxt.SetValue(str(total))
            self.enableTicketActions(True)
            self.enableTicketlineActions(False)

    def enableTicketActions(self, enable):
        self.closeBtn.Enable(enable)
        self.cancelBtn.Enable(enable)
        self.newTicketlineBtn.Enable(enable)

    def enableTicketlineActions(self, enable):
        self.plusBtn.Enable(enable)
        self.minusBtn.Enable(enable)
        self.editBtn.Enable(enable)

    ### Ticket Actions ###
    def _doCheckCurrentTicket(self):
        t = self.ticketChoice.getCurrentTicket()
        if t is None:
            wx.MessageBox('Select a ticket.', 'No ticket', wx.OK)
            return None
        else:
            return t

    def OnTicketChoice(self, event):
        event.Skip()
        t = self.ticketChoice.getCurrentTicket()
        self.setCurrentTicket(t)
    
    def OnNewButton(self, event):
        event.Skip()
        t = ticket.add(user=user.current)
        self.ticketChoice.updateList()
        self.setCurrentTicket(t)

    def OnCloseButton(self, event):
        event.Skip()
        t = self._doCheckCurrentTicket()
        if t:
            dlg = PayDialog(None, t)
            ret = dlg.ShowModal()
            if ret == wx.ID_OK:
                t.close()
                self.setCurrentTicket(None)

    def OnCancelButton(self, event):
        event.Skip()
        t = self._doCheckCurrentTicket()
        if t:
            t.delete()
            self.setCurrentTicket(None)

    ### Ticketline Actions ###
    def _doCheckCurrentTicketline(self):
        selected_indices = self.ticketList.getSelectedLines()
        if len(selected_indices) != 1:
            wx.MessageBox('Select a line.', 'No ticketline', wx.OK)
            return None
        else:
            tl = self.ticketList.getLine(selected_indices[0])
            return tl

    def _doChangeAmount(self, inc):
        t = self._doCheckCurrentTicket()
        tl = self._doCheckCurrentTicketline()
        if t and tl:
            new_amount = tl.data['amount']+inc
            if new_amount>0:
                p = tl.data['product']
                if p is not None and p.data['in_stock'] and p.data['quantity']<new_amount:
                    wx.MessageBox('Amount exceeds the product quantity in stock!', 'Warning', wx.OK | wx.ICON_WARNING)
                tl.update(amount=new_amount)
            else:
                tl.delete()
                self.enableTicketlineActions(False)
            self.ticketList.updateList(t, select=True)

    def OnTicketlineItemDeselect(self, event):
        event.Skip()
        self.enableTicketlineActions(False)
        
    def OnTicketlineItemSelect(self, event):
        event.Skip()
        self.enableTicketlineActions(True)

    def OnTicketlineItemActivate(self, event):
        event.Skip()
        self._doChangeAmount(+1)

    def OnTicketlineItemRightClick(self, event):
        event.Skip()
        self._doChangeAmount(-1)

    def OnNewTicketlineButton(self, event):
        event.Skip()
        t = self._doCheckCurrentTicket()
        if t:
            data = {'description': '', 'amount': 1, 'sell_price': 0, 'ticket': t,
                    'product': None, 'is_edited': True, 'user': user.current}
            dlg = EditDialog(None, data)
            ret = dlg.ShowModal()
            if ret == wx.ID_OK:
                tl = ticketline.add(**data)
                self.ticketList.updateList(t)
                index = self.ticketList.findLine(tl)
                self.ticketList.Select(index, True)
    
    def OnPlusButton(self, event):
        event.Skip()
        self._doChangeAmount(+1)

    def OnMinusButton(self, event):
        event.Skip()
        self._doChangeAmount(-1)

    def OnEditButton(self, event):
        event.Skip()
        t = self._doCheckCurrentTicket()
        tl = self._doCheckCurrentTicketline()
        if t and tl:
            data = tl.data.copy()
            dlg = EditDialog(None, data)
            ret = dlg.ShowModal()
            if ret == wx.ID_OK and tl.data != data:
                self.ticketList.editLine(tl, data)

    ### Catalog Actions ###
    def OnProductCatalogItemActivate(self, event):
        event.Skip()
        selected = self.catalogBook.productList.GetFirstSelected()
        p, image_id = self.catalogBook.productList.getItem(selected)
        if p is not None and image_id == 1:
            t = self._doCheckCurrentTicket()
            if t:
                self.ticketList.addProductLine(p)

    def OnCustomerCatalogItemActivate(self, event):
        event.Skip()
        selected = self.catalogBook.customerList.GetFirstSelected()
        c, image_id = self.catalogBook.customerList.getItem(selected)
        if c is not None and image_id == 1:
            t = self._doCheckCurrentTicket()
            if t:
                t.update(customer=c)
                self.customerTxt.SetValue(c.data['name'])

    ### Find Product Actions ###
    def OnF3Command(self, event):
        event.Skip()
        self.codeTxt.SelectAll()
        self.codeTxt.SetFocus()

    def OnCodeEnter(self, event):
        event.Skip()
        code = self.codeTxt.GetValue()
        p = product.find(code=code)
        if p is None:
            wx.MessageBox('Product with code %s not found.' % (code,), 'No match', wx.OK)
        else:
            t = self._doCheckCurrentTicket()
            if t:
                self.ticketList.addProductLine(p)
            self.codeTxt.SetValue('')
