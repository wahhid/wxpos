import wx

from pos.modules.customer.windows import CustomerCatalogList

from .pdf import PDFReportPanel
import pos.modules.report.objects.customers as customers_report
from pos.modules.report.dialogs import CustomerFilterDialog

class CustomersReportPanel(PDFReportPanel):
    def __init__(self, parent):
        PDFReportPanel.__init__(self, parent, validator=ParamValidator, showDateRange=True)

        self.catalogList = CustomerCatalogList(self.paramPanel)
        self.catalogList.SetValidator(ParamValidator(self, 'customer'))
        self.paramSizer.Add(self.catalogList, 0, flag=wx.EXPAND | wx.ALL)

        self.filterBtn = wx.Button(self.paramPanel, -1, label='Filter...')
        self.filterBtn.Bind(wx.EVT_BUTTON, self.OnFilterButton)
        self.paramSizer.Add(self.filterBtn, 0)

        self.parameters = {'customer': None, 'show_cash': False,
                           'show_cheque': False, 'show_card': False,
                           'show_debt': True, 'show_free': False,
                           'currency': None}

    def OnFilterButton(self, event):
        event.Skip()
        dlg = CustomerFilterDialog(self, ParamValidator)
        ret = dlg.ShowModal()

    def getFilename(self, from_date, to_date, customer,
                    show_cash, show_cheque, show_card, show_debt, show_free,
                    currency):
        show = (show_cash, show_cheque, show_card, show_debt, show_free)
        si = 0
        for i, s in enumerate(show):
            si += s*2**i
        if to_date is None:
            return 'customer-%s-%s-%d' % (customer.name, from_date, si)
        else:
            return 'customer-%s-%s-%s-%d' % (customer.name, from_date, to_date, si)

    def generateReport(self, filename, from_date, to_date, customer,
                       show_cash, show_cheque, show_card, show_debt, show_free,
                       currency):
        show = [('cash', show_cash), ('cheque', show_cheque), ('card', show_card),
                ('debt', show_debt), ('free', show_free)]
        show = filter(lambda s: s[1], show)
        show = map(lambda s: s[0], show)
        # TODO currency is not taken in consideration
        return customers_report.generateReport(filename, customer, from_date, to_date, show)

class ParamValidator(wx.PyValidator):
    def __init__(self, panel, key):
        wx.PyValidator.__init__(self)
        self.panel = panel
        self.key = key

    Clone = lambda self: ParamValidator(self.panel, self.key)

    def Validate(self, parent):
        try:
            win = self.GetWindow()
            data = self.getData(win)
            if self.key == 'customer':
                if data is None:
                    return False
                else:
                    return True
        except:
            print '-- ERROR -- in ParamValidator.Validate'
            print '--', self.key, self.panel.parameters
            raise
        return True

    def TransferFromWindow(self):
        try:
            win = self.GetWindow()
            data = self.getData(win)
            self.panel.parameters[self.key] = data
        except:
            print '-- ERROR -- in ParamValidator.TransferFromWindow'
            print '--', self.key, self.panel.parameters
            raise
        return True

    def TransferToWindow(self):
        try:
            win = self.GetWindow()
            data = self.panel.parameters[self.key]
            if self.key == 'customer':
                pass
            elif self.key.startswith('show_'):
                win.SetValue(data)
        except:
            print '-- ERROR -- in ParamValidator.TransferToWindow'
            print '--', self.key, self.panel.parameters
            raise
        return True
        
    def getData(self, win):
        data = None
        if self.key == 'customer':
            data = win.GetValue()
        elif self.key.startswith('show_'):
            data = win.IsChecked()
        return data
