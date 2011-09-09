import wx

import datetime
import os

from pos.modules.base.objects.idManager import ids

from pos.modules.customer.windows.customerCatalogList import CustomerCatalogList

from .pdf import PDFReportPanel
import pos.modules.report.objects.customers as customers_report

class CustomersReportPanel(PDFReportPanel):
    def __init__(self, parent):
        PDFReportPanel.__init__(self, parent, validator=ParamValidator, showDateRange=True)

        self.catalogList = CustomerCatalogList(self.parametersPanel)
        self.addParameter('Customer', self.catalogList, 'customer', style=wx.EXPAND | wx.ALL)
        
        self._init_sizers()

    def getFilename(self, from_date, to_date, customer):
        return 'customer-%s-%s-%s' % (customer.data['name'], from_date, to_date)

    def generateReport(self, filename, from_date, to_date, customer):
        return customers_report.generateReport(filename, customer, from_date, to_date)

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
            print '-- ERROR -- in ParamValidator.TransferToWindow'
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
        
    def getData(self, win):
        data = None
        if self.key == 'customer':
            selected = self.panel.catalogList.GetFirstSelected()
            item, image_id = self.panel.catalogList.getItem(selected)
            if image_id == 1:
                data = item
            else:
                data = None
        return data
