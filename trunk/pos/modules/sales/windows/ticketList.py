import wx
import wx.lib.mixins.listctrl as listmix

import pos

import pos.modules.currency.objects.currency as currency
from pos.modules.sales.objects.ticketline import TicketLine

class ListRowHighlighter(listmix.ListRowHighlighter):
    def RefreshRows(self):
        if 'gtk2' in wx.PlatformInfo:
            listmix.ListRowHighlighter.RefreshRows(self)
        else:
            wx.CallAfter(listmix.ListRowHighlighter.RefreshRows, self)

class TicketList(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, ListRowHighlighter):
    columns = ('Description', 'Price', 'Amount', 'Discount', 'Total')
    
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1,
                style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_SINGLE_SEL)#wx.LC_NO_HEADER | 

        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)
        
        ListRowHighlighter.__init__(self, mode=listmix.HIGHLIGHT_ODD)
        
        #listmix.CheckListCtrlMixin.__init__(self)
        #listmix.TextEditMixin.__init__(self)

        self.ticket = None
        self.lines = []
        for col, text in enumerate(self.columns):
            self.InsertColumn(col, text)

    # Product to Line manipulation
    def addProductLine(self, p):
        sell_price = currency.convert(p.price, p.currency, self.ticket.currency)
        tl = TicketLine()
        tl.update(description=p.name, sell_price=sell_price, amount=1, discount=0,
                  ticket=self.ticket, product=p, is_edited=False)
        self.updateList(self.ticket)
        index = self.findLine(tl)
        self.Select(index, True)

    def editLine(self, tl, data):
        p = tl.product
        if not tl.is_edited and p is not None:
            description_edited = (tl.description != data['description'])
            price_edited = (tl.sell_price != data['sell_price'])
            data.update({'is_edited': (description_edited or price_edited)})
            tl.update(**data)
        else:
            tl.update(**data)
        self.updateList(self.ticket, select=True)

    # Selection
    def getSelectedLines(self):
        selected = []
        index = -1
        while True:
            index = self.GetNextSelected(index)
            if index == -1:
                break
            selected.append(index)
        return selected

    def clearSelection(self):
        for index in self.GetItemCount():
            self.Select(index, False)

    # Lines
    def addLine(self, tl):
        self.lines.append(tl)
        items = self.getItemsFromLine(tl)
        index = self.Append(items)
        return index

    def clearLines(self):
        self.lines = []
        self.DeleteAllItems()

    def getLine(self, index):
        return self.lines[index]
        
    def findLine(self, tl):
        try:
            return self.lines.index(tl)
        except:
            return -1

    def getItemsFromLine(self, tl):
        c = self.ticket.currency
        items = [('* ' if tl.is_edited else '')+tl.description,
                 c.format(tl.sell_price),
                 'x%d' % (tl.amount,),
                 '%d%%' % (tl.discount*100,),
                 c.format(tl.total)]
        return items

    def updateList(self, t, select=False):
        selected_indices = self.getSelectedLines()
        if len(selected_indices) == 1:
            selected_tl = self.getLine(selected_indices[0])
        else:
            selected_tl = None
        self.clearLines()
        self.ticket = t
        for tl in self.ticket.ticketlines:
            self.addLine(tl)

        if select and selected_tl is not None:
            index = self.findLine(selected_tl)
            self.Select(index, True)

"""
    #self.Bind(wx.EVT_LIST_INSERT_ITEM, self._doUpdateWidth)
    #self.Bind(wx.EVT_LIST_DELETE_ITEM, self._doUpdateWidth)
    
    def _doUpdateWidth(self, event):
        event.Skip()
        if 'gtk2' in wx.PlatformInfo:
            self.updateWidth()
        else:
            wx.CallAfter(self.updateWidth)

    def updateWidth(self):
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        self.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
        self.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)
"""
