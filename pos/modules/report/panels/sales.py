import wx

import datetime

from pos.modules.base.objects.idManager import ids

import pos.modules.sales.objects.ticket as ticket
import pos.modules.sales.objects.ticketline as ticketline
from pos.modules.sales.windows.ticketList import TicketList

import pos.modules.report.objects.sales as sales_report

class SalesReportPanel(wx.Panel):
    def _init_sizers(self):
        self.controlsSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlsSizer.Add(self.fromLbl, 0, border=20, flag=wx.RIGHT)
        self.controlsSizer.Add(self.fromDp, 0, border=10, flag=wx.RIGHT)
        self.controlsSizer.Add(self.toLbl, 0, border=10, flag=wx.RIGHT)
        self.controlsSizer.Add(self.toDp, 0, border=10, flag=wx.RIGHT)
        self.controlsSizer.Add(self.generateBtn, 0, border=10, flag=wx.RIGHT)

        self.controlsPanel.SetSizer(self.controlsSizer)
        self.controlsSizer.Fit(self.controlsPanel)

        self.viewSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.viewSizer.Add(self.ticketList, 1, flag=wx.EXPAND | wx.ALL)

        self.viewPanel.SetSizer(self.viewSizer)
        self.viewSizer.Fit(self.viewPanel)
        
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.Add(self.controlsPanel, 0)
        self.mainSizer.Add(self.viewPanel, 1, border=10, flag=wx.EXPAND | wx.ALL)

        self.SetSizer(self.mainSizer)

    def _init_main(self):
        self.controlsPanel = wx.Panel(self, -1)
        self.viewPanel = wx.Panel(self, -1)

        self.fromLbl = wx.StaticText(self.controlsPanel, -1, label='Date Range')
        self.fromDp = wx.DatePickerCtrl(self.controlsPanel, -1, style=wx.DP_DROPDOWN)

        self.toLbl = wx.StaticText(self.controlsPanel, -1, label='To')
        self.toDp = wx.DatePickerCtrl(self.controlsPanel, -1, style=wx.DP_DROPDOWN | wx.DP_ALLOWNONE)
        
        self.generateBtn = wx.Button(self.controlsPanel, -1, label='Generate')
        self.generateBtn.Bind(wx.EVT_BUTTON, self.OnGenerateButton)

        self.ticketList = TicketList(self.viewPanel)
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)

        self._init_main()
        self._init_sizers()

    def OnGenerateButton(self, event):
        event.Skip()
        wx_from_date = self.fromDp.GetValue()
        from_date = datetime.datetime.fromtimestamp(wx_from_date.GetTicks())
        wx_to_date = self.toDp.GetValue()
        to_date = None if not wx_to_date.IsValid() else datetime.datetime.fromtimestamp(wx_to_date.GetTicks())

        ts = sales_report.getTickets(from_date, to_date)
        self.ticketList.clearLines()
        for t in ts:
            for tl in ticketline.find(ticket=t):
                self.ticketList.addLine(tl)
