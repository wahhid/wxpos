import wx

import pos.modules.currency.objects.currency as currency

import pos.modules.sales.objects.ticketline as ticketline

from pos.modules.base.objects.idManager import ids

from ..windows.ticketList import TicketList

class PayDialog(wx.Dialog):
    def __init_ctrls(self):
        self.ticketList = TicketList(self)
        
        # total/given/change
        self.givenLbl = wx.StaticText(self, -1, label='Given')
        self.givenTxt = wx.TextCtrl(self, -1)
        self.givenTxt.Bind(wx.EVT_TEXT, self.OnGivenText)
        
        self.totalLbl = wx.StaticText(self, -1, label='Total')
        self.totalTxt = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        
        self.separationLine = wx.StaticLine(self, -1)

        self.changeLbl = wx.StaticText(self, -1, label='Change')
        self.changeTxt = wx.TextCtrl(self, -1, style=wx.TE_READONLY)

        self.okBtn = wx.Button(self, wx.ID_OK, label='OK')
        self.okBtn.Bind(wx.EVT_BUTTON, self.OnOkButton)
        
        self.printBtn = wx.Button(self, -1, label='Print')
        self.printBtn.Bind(wx.EVT_BUTTON, self.OnPrintButton)

        self.cancelBtn = wx.Button(self, wx.ID_CANCEL, label='Cancel')
    
    def __init_sizers(self):
        self.formSizer = wx.GridBagSizer(hgap=5, vgap=5)
        
        fields = [(self.ticketList,),
                  (self.givenLbl, self.givenTxt),
                  (self.totalLbl, self.totalTxt),
                  (self.separationLine,),
                  (self.changeLbl, self.changeTxt)]
        for row, f in enumerate(fields):
            if len(f) == 2:
                self.formSizer.Add(f[0], (row, 0), flag=wx.EXPAND | wx.ALL)
                self.formSizer.Add(f[1], (row, 1), flag=wx.ALIGN_RIGHT)
            else:
                self.formSizer.Add(f[0], (row, 0), (1, 2), flag=wx.EXPAND | wx.ALL)
        self.formSizer.AddGrowableRow(0, 1)
        self.formSizer.AddGrowableCol(1, 1)

        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL)
        self.controlSizer.Add(self.okBtn, 0, flag=wx.CENTER | wx.ALL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL)
        self.controlSizer.Add(self.printBtn, 0, flag=wx.CENTER | wx.ALL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL)
        self.controlSizer.Add(self.cancelBtn, 0, flag=wx.CENTER | wx.ALL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL) 
        
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.AddSizer(self.formSizer, 1, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.AddSizer(self.controlSizer, 0, border=10, flag=wx.BOTTOM | wx.LEFT | wx.RIGHT | wx.EXPAND)
        self.SetSizer(self.mainSizer)
    
    def __init__(self, parent, t):
        wx.Dialog.__init__(self, parent, ids['editTicketlineDialog'],
              size=wx.Size(400, 500), title='Pay ticket')

        self.ticket = t
        self.__init_ctrls()
        self.__init_sizers()
        
        self.total = self.getTicketTotal()
        self.given = self.total
        self.change = 0

        tc = self.ticket.data['currency']
        self.givenTxt.SetValue(str(self.given))
        self.totalTxt.SetValue(tc.format(self.total))
        self.changeTxt.SetValue(tc.format(self.change))
        
        self.ticketList.updateList(self.ticket)
    
    # Ticketline-related
    def getTicketTotal(self):
        tls = ticketline.find(list=True, ticket=self.ticket)
        total = 0
        for tl in tls:
            total += tl.data['amount']*tl.data['sell_price']
        return total

    def OnGivenText(self, event):
        event.Skip()
        try:
            self.given = float(self.givenTxt.GetValue())
        except:
            self.given = 0
        self.change = self.given-self.total
        
        tc = self.ticket.data['currency']
        self.changeTxt.SetValue(tc.format(self.change))

    def OnPrintButton(self, event):
        wx.MessageBox('Not implemented yet.', 'Print ticket', style=wx.OK)
        event.Skip()

    def OnOkButton(self, event):
        tc = self.ticket.data['currency']
        if self.given < self.total:
            wx.MessageBox('Not enough. %s remaining.' % (tc.format(-self.change),), 'Pay Ticket', style=wx.OK)
        elif self.given > self.total:
            retCode = wx.MessageBox('Return change: %s.' % (tc.format(self.change),), 'Pay Ticket', style=wx.OK | wx.CANCEL)
            if retCode == wx.OK:
                event.Skip()
        else:
            event.Skip()
