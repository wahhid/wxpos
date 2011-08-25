import wx

import pos.modules.user.objects.user as user

import pos.modules.customer.objects.customer as customer

import pos.modules.stock.objects.category as category
import pos.modules.stock.objects.product as product

import pos.modules.sales.objects.ticket as ticket
import pos.modules.sales.objects.ticketline as ticketline

from .editDialog import EditDialog
from .payDialog import PayDialog
from .ticketList import TicketList

from pos.modules.base.objects.idManager import ids

class SalesPanel(wx.Panel):
    def _init_sizers(self):
        self.findSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.findSizer.Add(self.codeTxt, 0)
        self.findSizer.Add(self.findBtn, 0)

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
        self.tActionSizer.Add(self.customerChoice, 0, border=3, flag=wx.ALL | wx.EXPAND)

        self.mainSizer = wx.GridBagSizer(hgap=0, vgap=0)
        self.mainSizer.AddSizer(self.tlActionSizer, (1, 0), (1, 1))
        self.mainSizer.AddSizer(self.tActionSizer, (0, 1), (1, 1))
        self.mainSizer.Add(self.ticketList, (1, 1), (1, 1), flag=wx.EXPAND | wx.ALL)
        self.mainSizer.AddSizer(self.findSizer, (1, 2), flag=wx.ALIGN_BOTTOM)
        self.mainSizer.Add(self.catalogList, (2, 0), (1, 3), flag=wx.EXPAND | wx.ALL)
        
        self.mainSizer.AddGrowableCol(1, 1)
        self.mainSizer.AddGrowableRow(1, 1)
        self.mainSizer.AddGrowableRow(2, 2)

        self.SetSizer(self.mainSizer)

    def _init_ctrls(self):
        ### Ticket actions ###
        self.newBtn = wx.BitmapButton(self, -1,
                    bitmap=wx.Bitmap('./images/commands/add.png', wx.BITMAP_TYPE_PNG),
                    style=wx.BU_AUTODRAW)
        self.newBtn.Bind(wx.EVT_BUTTON, self.OnNewButton)

        self.closeBtn = wx.BitmapButton(self, -1,
                    bitmap=wx.Bitmap('./images/commands/load.png', wx.BITMAP_TYPE_PNG),
                    style=wx.BU_AUTODRAW)
        self.closeBtn.Bind(wx.EVT_BUTTON, self.OnCloseButton)

        self.cancelBtn = wx.BitmapButton(self, -1,
                    bitmap=wx.Bitmap('./images/commands/cancel.png', wx.BITMAP_TYPE_PNG),
                    style=wx.BU_AUTODRAW)
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancelButton)
        
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

    def _init_main(self):
        self.ticketList = TicketList(self)
        self.ticketList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnTicketlineItemActivate)
        self.ticketList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnTicketlineItemSelect)
        self.ticketList.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnTicketlineItemDeselect)

        self.codeTxt = wx.TextCtrl(self, -1)
        self.findBtn = wx.BitmapButton(self, -1,
                    bitmap=wx.Bitmap('./images/commands/search.png', wx.BITMAP_TYPE_PNG),
                    style=wx.BU_AUTODRAW)
        self.findBtn.Bind(wx.EVT_BUTTON, self.OnFindButton)
        
        self.ticketChoice = TicketChoice(self)
        self.ticketChoice.Bind(wx.EVT_CHOICE, self.OnTicketChoice)

        self.customerChoice = CustomerChoice(self)
        self.customerChoice.Bind(wx.EVT_CHOICE, self.OnCustomerChoice)

        self._init_ctrls()
        
        self.catalogList = CatalogList(self)
        self.catalogList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnCatalogItemActivate)
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, ids['salesPanel'],
                style=wx.TAB_TRAVERSAL)

        self._init_main()
        self._init_sizers()

        self.enableTicketActions(False)
        self.enableTicketlineActions(False)

        self.ticketChoice.updateList()
        self.customerChoice.updateList()

    def setCurrentTicket(self, t):
        if t is None:
            self.ticketChoice.updateList()
            self.ticketList.clearLines()
            self.enableTicketActions(False)
            self.enableTicketlineActions(False)
        else:
            self.ticketChoice.setCurrentTicket(t)
            self.ticketList.updateList(t)
            self.enableTicketActions(True)
            self.enableTicketlineActions(False)

    def enableTicketActions(self, enable):
        self.closeBtn.Enable(enable)
        self.cancelBtn.Enable(enable)

    def enableTicketlineActions(self, enable):
        self.plusBtn.Enable(enable)
        self.minusBtn.Enable(enable)
        self.editBtn.Enable(enable)

    def _doCheckCurrentTicket(self):
        t = self.ticketChoice.getCurrentTicket()
        if t is None:
            wx.MessageBox('Select a ticket.', 'No ticket', wx.OK)
            return None
        else:
            return t

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
                tl.update(amount=new_amount)
            else:
                tl.delete()
                self.enableTicketlineActions(False)
            self.ticketList.updateList(t, select=True)

    def OnFindButton(self, event):
        event.Skip()

    # Ticket-related
    def OnTicketChoice(self, event):
        event.Skip()
        t = self.ticketChoice.getCurrentTicket()
        self.setCurrentTicket(t)

    def OnCustomerChoice(self, event):
        event.Skip()
        c = self.customerChoice.getCurrentCustomer()
        t = self._doCheckCurrentTicket()
        if t and c is not None:
            t.setCustomer(c)
    
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

    # Ticketline-related
    def OnCatalogItemActivate(self, event):
        selected = self.catalogList.GetFirstSelected()
        p = self.catalogList.getItem(selected)
        if isinstance(p, product.Product):
            t = self._doCheckCurrentTicket()
            if t:
                tl = ticketline.add(description=p.data['name'], sell_price=p.data['price'],
                                    amount=1, ticket=t, product=p, is_edited=False)
                self.ticketList.updateList(t)
                index = self.ticketList.findLine(tl)
                self.ticketList.Select(index, True)
        else:
            event.Skip()

    def OnTicketlineItemDeselect(self, event):
        event.Skip()
        self.enableTicketlineActions(False)
        
    def OnTicketlineItemSelect(self, event):
        event.Skip()
        self.enableTicketlineActions(True)

    def OnTicketlineItemActivate(self, event):
        event.Skip()
        self._doChangeAmount(+1)
    
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
                p = tl.data['product']
                if not tl.data['is_edited'] and p is not None:
                    is_edited = tl.data['description'] != data['description'] or tl.data['sell_price'] != data['sell_price']
                    data.update({'is_edited': is_edited})
                    tl.update(**data)
                else:
                    tl.update(**data)
                self.ticketList.updateList(t, select=True)

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

class TicketChoice(wx.Choice):
    def __init__(self, parent):
        wx.Choice.__init__(self, parent, -1)

        self.__tickets = {}

    def setCurrentTicket(self, t):
        self.SetStringSelection(self.getTicketLabel(t))

    def getCurrentTicket(self):
        ch = self.GetStringSelection()
        try:
            return self.__tickets[ch]
        except KeyError:
            return None

    def getTicketLabel(self, t):
        return 'Ticket #%.3d' % (t.id,)

    def updateList(self):
        choices = []
        self.__tickets = {}
        ts = ticket.find(list=True, closed=False)
        for t in ts:
            ch = self.getTicketLabel(t)
            self.__tickets[ch] = t
            choices.append(ch)
        self.SetItems(choices)

class CustomerChoice(wx.Choice):
    def __init__(self, parent):
        wx.Choice.__init__(self, parent, -1)

        self.__customers = {}

    def setCurrentCustomer(self, c):
        self.SetStringSelection(self.getCustomerLabel(c))

    def getCurrentCustomer(self):
        ch = self.GetStringSelection()
        try:
            return self.__customers[ch]
        except KeyError:
            return None

    def getCustomerLabel(self, c):
        return '%s' % (c.data['name'],)

    def updateList(self):
        choices = []
        self.__customers = {}
        cs = customer.find(list=True)
        for c in cs:
            ch = self.getCustomerLabel(c)
            self.__customers[ch] = c
            choices.append(ch)
        self.SetItems(choices)

class CatalogList(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_ICON | wx.LC_AUTOARRANGE | wx.LC_SINGLE_SEL)
        
        il = wx.ImageList(32,32, True)
        
        #bmp = wx.Bitmap(name, wx.BITMAP_TYPE_PNG)
        category_bmp = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, size=(32, 32))
        product_bmp = wx.ArtProvider.GetBitmap(wx.ART_HELP_BOOK, size=(32, 32))
        up_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DIR_UP, size=(32, 32))
        
        il.Add(category_bmp)
        il.Add(product_bmp)
        il.Add(up_bmp)

        self.AssignImageList(il, wx.IMAGE_LIST_NORMAL)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivate)

        self.__view = []
        self.__current = None
        self.updateList(None)

    def getItem(self, index):
        return self.__view[index]

    def clearCatalog(self):
        self.DeleteAllItems()
        self.__view = []

    def OnItemActivate(self, event):
        selected = self.GetFirstSelected()
        item = self.getItem(selected)
        if item is None:
            parent = self.__current.data['parent_category']
            self.updateList(parent)
        elif isinstance(item, category.Category):
            self.updateList(item)
        else:
            event.Skip()

    def updateList(self, parent):
        self.__current = parent
        
        child_categories = category.find(list=True, parent_category=parent)
        child_products = product.find(list=True, category=parent)

        self.clearCatalog()
        index = -1
        if parent is not None:
            index = self.InsertImageStringItem(0, '< Up', 2)
            self.__view.append(None)
        _last_index = index+1
        for index, c in enumerate(child_categories):
            index = self.InsertImageStringItem(index+_last_index, c.data['name'], 0)
            self.__view.append(c)
        _last_index = index+1
        for index, p in enumerate(child_products):
            index = self.InsertImageStringItem(index+_last_index, p.data['name'], 1)
            self.__view.append(p)
