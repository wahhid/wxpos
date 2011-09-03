import wx

import pos.modules.sales.objects.ticket as ticket

from pos.modules.base.objects.idManager import ids

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
