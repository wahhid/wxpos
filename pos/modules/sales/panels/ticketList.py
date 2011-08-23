import wx
import wx.lib.mixins.listctrl as listmix

import pos.modules.currency.objects.currency as currency

import pos.modules.sales.objects.ticketline as ticketline

from pos.modules.base.objects.idManager import ids

class ListRowHighlighter(listmix.ListRowHighlighter):
    def RefreshRows(self):
        if 'gtk2' in wx.PlatformInfo:
            listmix.ListRowHighlighter.RefreshRows(self)
        else:
            wx.CallAfter(listmix.ListRowHighlighter.RefreshRows, self)

class TicketList(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, ListRowHighlighter):
    columns = ('Description', 'Price', 'Amount', 'Total')
    
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1,
                style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_SINGLE_SEL)#wx.LC_NO_HEADER | 

        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)
        
        ListRowHighlighter.__init__(self, mode=listmix.HIGHLIGHT_ODD)
        
        #listmix.CheckListCtrlMixin.__init__(self)
        #listmix.TextEditMixin.__init__(self)
        
        self.lines = []
        for col, text in enumerate(self.columns):
            self.InsertColumn(col, text)

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
        description = tl.data['description']
        p = tl.data['product']
        if p is None:
            sell_price = tl.data['sell_price']
        else:
            sell_price = currency.convert(tl.data['sell_price'],
                            p.data['currency'], currency.default)
        amount = tl.data['amount']
        currency_symbol = currency.default.data['symbol']
        items = [description,
                 '%d %s' % (sell_price, currency_symbol),
                 'x%d' % (amount,),
                 '%d %s' % (amount*sell_price, currency_symbol)]
        return items

    def updateList(self, t, select=False):
        selected_indices = self.getSelectedLines()
        if len(selected_indices) == 1:
            selected_tl = self.getLine(selected_indices[0])
        else:
            selected_tl = None
        self.clearLines()
        tls = ticketline.find(list=True, ticket=t)
        for tl in tls:
            self.addLine(tl)

        if select and selected_tl is not None:
            selected_tl = ticketline.find(_id=selected_tl.id)
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
