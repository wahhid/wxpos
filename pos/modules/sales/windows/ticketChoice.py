import wx

import pos

from pos.modules.sales.objects.ticket import Ticket

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
        return 'Ticket %s' % (t.display,)

    def updateList(self):
        choices = []
        self.__tickets = {}
        session = pos.database.session()
        ts = session.query(Ticket).filter(~Ticket.closed).all()
        for t in ts:
            ch = self.getTicketLabel(t)
            self.__tickets[ch] = t
            choices.append(ch)
        self.SetItems(choices)
