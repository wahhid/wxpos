import wx

import pos.modules.currency.objects.currency as currency

import pos.modules.sales.objects.ticketline as ticketline

from pos.modules.base.objects.idManager import ids

import pos.menu

class PayDialog(wx.Dialog):
    def __init_ctrls(self, disabled):
        self.totalLbl = wx.StaticText(self, -1, label='Due Amount')
        self.totalTxt = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        
        self.separationLine = wx.StaticLine(self, -1)

        self.mainToolbook = wx.Toolbook(self, -1, style=wx.BK_LEFT)
        ## TEST TODO
        self.mainToolbook.AssignImageList(pos.menu.il)

        toolbar = self.mainToolbook.GetToolBar()
        selected = None
        panels = (CashPanel, ChequePanel, CardPanel, VoucherPanel, FreePanel, DebtPanel)
        for p, panel_class in enumerate(panels):
            panel = panel_class(self.mainToolbook, self)
            self.mainToolbook.AddPage(imageId=0, page=panel, select=False, text=panel.label)
            if not panel.IsAllowed() or panel.payment[0] in disabled:
                toolbar.EnableTool(p+1, False)
            elif selected is None:
                selected = p
                self.mainToolbook.ChangeSelection(p)

        self.okBtn = wx.Button(self, wx.ID_OK, label='OK')
        self.okBtn.Bind(wx.EVT_BUTTON, self.OnOkButton)
        
        self.printBtn = wx.Button(self, -1, label='Print')
        self.printBtn.Bind(wx.EVT_BUTTON, self.OnPrintButton)

        self.cancelBtn = wx.Button(self, wx.ID_CANCEL, label='Cancel')
    
    def __init_sizers(self):
        self.topSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.topSizer.Add(self.totalLbl, 1, flag=wx.EXPAND | wx.ALL)
        self.topSizer.Add(self.totalTxt, 0, flag=wx.ALIGN_RIGHT)

        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL)
        self.controlSizer.Add(self.okBtn, 0, flag=wx.CENTER | wx.ALL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL)
        self.controlSizer.Add(self.printBtn, 0, flag=wx.CENTER | wx.ALL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL)
        self.controlSizer.Add(self.cancelBtn, 0, flag=wx.CENTER | wx.ALL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL) 
        
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.AddSizer(self.topSizer, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.mainToolbook, 1, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.Add(self.separationLine, 0, border=5, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.AddSizer(self.controlSizer, 0, border=10, flag=wx.BOTTOM | wx.LEFT | wx.RIGHT | wx.EXPAND)
        self.SetSizer(self.mainSizer)
    
    def __init__(self, parent, total, _currency, _customer, disabled=[]):
        wx.Dialog.__init__(self, parent, ids['editTicketlineDialog'],
              size=wx.Size(400, 500), title='Pay ticket')

        self.total = total
        self.currency = _currency
        self.customer = _customer
        self.payment = None
        
        self.__init_ctrls(disabled)
        self.__init_sizers()

        self.totalTxt.SetValue(self.currency.format(self.total))

    def OnPrintButton(self, event):
        wx.MessageBox('Not implemented yet.', 'Print ticket', style=wx.OK)
        event.Skip()

    def OnOkButton(self, event):
        sel = self.mainToolbook.GetSelection()
        panel = self.mainToolbook.GetPage(sel)
        if panel.Ok():
            self.payment = panel.payment
            event.Skip()

class CashPanel(wx.Panel):
    label = "Cash"
    payment = ("cash", True)
    def __init_ctrls(self):
        self.givenLbl = wx.StaticText(self, -1, label='Given')
        self.givenTxt = wx.TextCtrl(self, -1)
        self.givenTxt.Bind(wx.EVT_TEXT, self.OnGivenText)

        self.changeLbl = wx.StaticText(self, -1, label='Change')
        self.changeTxt = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
    
    def __init_sizers(self):
        self.formSizer = wx.GridBagSizer(hgap=5, vgap=5)
        
        fields = [(self.givenLbl, self.givenTxt),
                  (self.changeLbl, self.changeTxt)]
        for row, f in enumerate(fields):
            if len(f) == 2:
                self.formSizer.Add(f[0], (row, 0), flag=wx.EXPAND | wx.ALL)
                self.formSizer.Add(f[1], (row, 1), flag=wx.ALIGN_RIGHT)
            else:
                self.formSizer.Add(f[0], (row, 0), (1, 2), flag=wx.EXPAND | wx.ALL)
        self.formSizer.AddGrowableRow(0, 1)
        self.formSizer.AddGrowableCol(1, 1)
        self.SetSizer(self.formSizer)
    
    def __init__(self, parent, dialog):
        wx.Panel.__init__(self, parent, -1)

        self.dialog = dialog
        
        self.__init_ctrls()
        self.__init_sizers()

        self.given = self.dialog.total
        self.change = 0

        tc = self.dialog.currency
        self.givenTxt.SetValue(str(self.given))
        self.changeTxt.SetValue(tc.format(self.change))

    def IsAllowed(self):
        return True

    def Ok(self):
        if self.given < self.dialog.total:
            tc = self.dialog.currency
            wx.MessageBox('Not enough. %s remaining.' % (tc.format(-self.change),), 'Pay Ticket', style=wx.OK)
            return False
        elif self.given > self.dialog.total:
            tc = self.dialog.currency
            retCode = wx.MessageBox('Return change: %s.' % (tc.format(self.change),), 'Pay Ticket', style=wx.OK | wx.CANCEL)
            if retCode == wx.OK:
                return True
            else:
                return False
        else:
            return True

    def OnGivenText(self, event):
        event.Skip()
        try:
            self.given = float(self.givenTxt.GetValue())
        except:
            self.given = 0
        self.change = self.given-self.dialog.total
        
        tc = self.dialog.currency
        self.changeTxt.SetValue(tc.format(self.change))

class ChequePanel(wx.Panel):
    label = "Cheque"
    payment = ("cheque", True)
    def __init_ctrls(self):
        self.givenLbl = wx.StaticText(self, -1, label='Given')
        self.givenTxt = wx.TextCtrl(self, -1)
    
    def __init_sizers(self):
        self.formSizer = wx.GridBagSizer(hgap=5, vgap=5)
        
        fields = [(self.givenLbl, self.givenTxt)]
        for row, f in enumerate(fields):
            if len(f) == 2:
                self.formSizer.Add(f[0], (row, 0), flag=wx.EXPAND | wx.ALL)
                self.formSizer.Add(f[1], (row, 1), flag=wx.ALIGN_RIGHT)
            else:
                self.formSizer.Add(f[0], (row, 0), (1, 2), flag=wx.EXPAND | wx.ALL)
        self.formSizer.AddGrowableRow(0, 1)
        self.formSizer.AddGrowableCol(1, 1)
        self.SetSizer(self.formSizer)
    
    def __init__(self, parent, dialog):
        wx.Panel.__init__(self, parent, -1)

        self.dialog = dialog
        
        self.__init_ctrls()
        self.__init_sizers()

        self.given = self.dialog.total

        tc = self.dialog.currency
        self.givenTxt.SetValue(str(self.given))

    def IsAllowed(self):
        return True

    def Ok(self):
        if self.given < self.dialog.total:
            tc = self.dialog.currency
            wx.MessageBox('Not enough. %s remaining.' % (tc.format(-self.change),), 'Pay Ticket', style=wx.OK)
            return False
        elif self.given > self.dialog.total:
            tc = self.dialog.currency
            retCode = wx.MessageBox('Return change: %s.' % (tc.format(self.change),), 'Pay Ticket', style=wx.OK | wx.CANCEL)
            if retCode == wx.OK:
                return True
            else:
                return False
        else:
            return True

class VoucherPanel(wx.Panel):
    label = "Voucher"
    payment = ("voucher", True)
    def __init_ctrls(self):
        self.givenLbl = wx.StaticText(self, -1, label='Given')
        self.givenTxt = wx.TextCtrl(self, -1)
        self.givenTxt.Bind(wx.EVT_TEXT, self.OnGivenText)

        self.changeLbl = wx.StaticText(self, -1, label='Change')
        self.changeTxt = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
    
    def __init_sizers(self):
        self.formSizer = wx.GridBagSizer(hgap=5, vgap=5)
        
        fields = [(self.givenLbl, self.givenTxt),
                  (self.changeLbl, self.changeTxt)]
        for row, f in enumerate(fields):
            if len(f) == 2:
                self.formSizer.Add(f[0], (row, 0), flag=wx.EXPAND | wx.ALL)
                self.formSizer.Add(f[1], (row, 1), flag=wx.ALIGN_RIGHT)
            else:
                self.formSizer.Add(f[0], (row, 0), (1, 2), flag=wx.EXPAND | wx.ALL)
        self.formSizer.AddGrowableRow(0, 1)
        self.formSizer.AddGrowableCol(1, 1)
        self.SetSizer(self.formSizer)
    
    def __init__(self, parent, dialog):
        wx.Panel.__init__(self, parent, -1)

        self.dialog = dialog
        
        self.__init_ctrls()
        self.__init_sizers()

        self.given = self.dialog.total
        self.change = 0

        tc = self.dialog.currency
        self.givenTxt.SetValue(str(self.given))
        self.changeTxt.SetValue(tc.format(self.change))

    def IsAllowed(self):
        return True

    def Ok(self):
        if self.given < self.dialog.total:
            tc = self.dialog.currency
            wx.MessageBox('Not enough. %s remaining.' % (tc.format(-self.change),), 'Pay Ticket', style=wx.OK)
            return False
        elif self.given > self.dialog.total:
            tc = self.dialog.currency
            retCode = wx.MessageBox('Return change: %s.' % (tc.format(self.change),), 'Pay Ticket', style=wx.OK | wx.CANCEL)
            if retCode == wx.OK:
                return True
            else:
                return False
        else:
            return True

    def OnGivenText(self, event):
        event.Skip()
        try:
            self.given = float(self.givenTxt.GetValue())
        except:
            self.given = 0
        self.change = self.given-self.dialog.total

        tc = self.dialog.currency
        self.changeTxt.SetValue(tc.format(self.change))

class CardPanel(wx.Panel):
    label = "Card"
    payment = ("card", True)
    def __init_ctrls(self):
        self.infoLbl = wx.StaticText(self, -1, label='Not implemented yet.')
    
    def __init_sizers(self):
        self.formSizer = wx.GridBagSizer(hgap=5, vgap=5)
        
        fields = [(self.infoLbl,)]
        for row, f in enumerate(fields):
            if len(f) == 2:
                self.formSizer.Add(f[0], (row, 0), flag=wx.EXPAND | wx.ALL)
                self.formSizer.Add(f[1], (row, 1), flag=wx.ALIGN_RIGHT)
            else:
                self.formSizer.Add(f[0], (row, 0), (1, 2), flag=wx.EXPAND | wx.ALL)
        self.formSizer.AddGrowableRow(0, 1)
        self.formSizer.AddGrowableCol(1, 1)
        self.SetSizer(self.formSizer)
    
    def __init__(self, parent, dialog):
        wx.Panel.__init__(self, parent, -1)

        self.dialog = dialog
        
        self.__init_ctrls()
        self.__init_sizers()

    def IsAllowed(self):
        return True

    def Ok(self):
        wx.MessageBox('Card payment not implemented yet.', 'Pay Ticket', style=wx.OK)
        return False

class FreePanel(wx.Panel):
    label = "Free"
    payment = ("free", False)
    def __init_ctrls(self):
        self.infoLbl = wx.StaticText(self, -1, label='It\'s on the house.')
    
    def __init_sizers(self):
        self.formSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.formSizer.Add(self.infoLbl, 1, border=5, flag=wx.EXPAND | wx.ALL)
        self.SetSizer(self.formSizer)
    
    def __init__(self, parent, dialog):
        wx.Panel.__init__(self, parent, -1)

        self.dialog = dialog
        
        self.__init_ctrls()
        self.__init_sizers()

    def IsAllowed(self):
        return self.dialog.customer is not None

    def Ok(self):
        wx.MessageBox('Card payment not implemented yet.', 'Pay Ticket', style=wx.OK)
        return False

class DebtPanel(wx.Panel):
    label = "Debt"
    payment = ("debt", False)
    def __init_ctrls(self):
        self.debtLbl = wx.StaticText(self, -1, label='Debt')
        self.debtTxt = wx.TextCtrl(self, -1, style=wx.TE_READONLY)

        self.nameLbl = wx.StaticText(self, -1, label='Name')
        self.nameTxt = wx.TextCtrl(self, -1, style=wx.TE_READONLY)

        self.maxDebtLbl = wx.StaticText(self, -1, label='Max Debt')
        self.maxDebtTxt = wx.TextCtrl(self, -1, style=wx.TE_READONLY)

        self.currentDebtLbl = wx.StaticText(self, -1, label='Current Debt')
        self.currentDebtTxt = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
    
    def __init_sizers(self):
        self.formSizer = wx.GridBagSizer(hgap=5, vgap=5)
        
        fields = [(self.debtLbl, self.debtTxt),
                  (self.nameLbl, self.nameTxt),
                  (self.maxDebtLbl, self.maxDebtTxt),
                  (self.currentDebtLbl, self.currentDebtTxt)]
        for row, f in enumerate(fields):
            if len(f) == 2:
                self.formSizer.Add(f[0], (row, 0), flag=wx.EXPAND | wx.ALL)
                self.formSizer.Add(f[1], (row, 1), flag=wx.ALIGN_RIGHT)
            else:
                self.formSizer.Add(f[0], (row, 0), (1, 2), flag=wx.EXPAND | wx.ALL)
        self.formSizer.AddGrowableRow(0, 1)
        self.formSizer.AddGrowableCol(1, 1)
        self.SetSizer(self.formSizer)
    
    def __init__(self, parent, dialog):
        wx.Panel.__init__(self, parent, -1)

        self.dialog = dialog
        
        self.__init_ctrls()
        self.__init_sizers()

        self.debt = self.dialog.total

        tc = self.dialog.currency
        self.debtTxt.SetValue(tc.format(self.debt))

        c = self.dialog.customer
        if c is not None:
            self.nameTxt.SetValue(c.data['name'])
            self.maxDebtTxt.SetValue(str(c.data['max_debt']))

    def IsAllowed(self):
        return self.dialog.customer is not None

    def Ok(self):
        c = self.dialog.customer
        if c is None:
            wx.MessageBox('No customer assigned', 'Pay Ticket', style=wx.OK)
            return False
        else:
            return True
