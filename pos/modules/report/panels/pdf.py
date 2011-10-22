import wx

import os

from pos.modules.report.windows.dateRange import DateRange

from pos.modules.base.objects.idManager import ids

try:
    from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel
    can_view_pdf = True
except:
    can_view_pdf = False

class PDFReportPanel(wx.Panel):
    def _init_sizers(self):
        self.paramSizer = wx.BoxSizer(orient=wx.VERTICAL)
        
        # DATE RANGE
        if self.show_date_range:
            self.paramSizer.Add(self.dateRange, 1, flag=wx.EXPAND | wx.ALL)
        
        self.paramPanel.SetSizer(self.paramSizer)

        # PDF VIEWER
        self.viewSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.viewSizer.Add(self.pdfViewer, 1, flag=wx.EXPAND | wx.ALL)

        self.viewPanel.SetSizer(self.viewSizer)
        self.viewSizer.Fit(self.viewPanel)

        # CONTROLS
        self.controlsSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlsSizer.Add(self.generateBtn, 0, border=10, flag=wx.RIGHT)# | wx.ALIGN_RIGHT)
        self.controlsSizer.Add(self.printBtn, 0, border=10, flag=wx.RIGHT)# | wx.ALIGN_RIGHT)

        self.controlsPanel.SetSizer(self.controlsSizer)
        self.controlsSizer.Fit(self.controlsPanel)

        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.Add(self.paramPanel, 0, border=10, flag=wx.EXPAND | wx.ALL)
        self.mainSizer.Add(self.viewPanel, 1, border=10, flag=wx.EXPAND | wx.ALL)
        self.mainSizer.Add(self.controlsPanel, 0, border=10, flag=wx.ALIGN_RIGHT | wx.ALL)

        self.SetSizer(self.mainSizer)

    def _init_main(self):
        self.paramPanel = wx.Panel(self, -1)
        self.viewPanel = wx.Panel(self, -1)
        self.controlsPanel = wx.Panel(self, -1)

        if self.show_date_range:
            self.dateRange = DateRange(self.paramPanel, -1)

        if can_view_pdf:
            self.pdfViewer = pdfViewer(self.viewPanel, -1, wx.DefaultPosition, wx.DefaultSize, style=0)
        else:
            self.pdfViewer = wx.StaticText(self.viewPanel, -1, label='wxPython version 2.9 is required to preview pdf files.')
        
        self.generateBtn = wx.Button(self.controlsPanel, -1, label='Generate')
        self.generateBtn.Bind(wx.EVT_BUTTON, self.OnGenerateButton)

        self.printBtn = wx.Button(self.controlsPanel, -1, label='Print')
        self.printBtn.Bind(wx.EVT_BUTTON, self.OnPrintButton)

    def __init__(self, parent, validator=None, showDateRange=True):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)

        self.show_date_range = showDateRange
        self.parameters = {}

        self._init_main()
        self._init_sizers()

    def _generateReport(self):
        self.paramPanel.TransferDataFromWindow()
        parameters = self.parameters.copy()
        if self.show_date_range:
            from_date, to_date = self.dateRange.GetValue()

        parameters.update({'from_date': from_date, 'to_date': to_date})

        filename = './reports/%s.pdf' % (self.getFilename(**parameters),)
        filename = os.path.abspath(filename)

        doc = self.generateReport(filename, **parameters)
        if doc is None:
            return None
        else:
            return filename

    def getFilename(self, **parameters):
        return 'default-name'

    def generateReport(self, filename, **parmeters):
        return None

    def OnGenerateButton(self, event):
        event.Skip()

        if not self.paramPanel.Validate():
            wx.MessageBox('Invalid parmaeters.', 'Generate Report', style=wx.OK | wx.ICON_INFORMATION)
            return
        
        filename = self._generateReport()
        if filename is None:
            wx.MessageBox('An error occured while generating the report.', 'Generate Report', style=wx.OK | wx.ICON_ERROR)
            return
        
        if can_view_pdf:
            self.pdfViewer.LoadFile(filename)
        else:
            retCode = wx.MessageBox('Print using default printer?', 'Generate Report', style=wx.YES_NO | wx.ICON_QUESTION)
            if retCode == wx.YES:
                os.startfile(filename, 'print')
            else:
                os.startfile(filename)

    def OnPrintButton(self, event):
        event.Skip()
        wx.MessageBox('Not implemented yet.', 'Print report', style=wx.OK)
