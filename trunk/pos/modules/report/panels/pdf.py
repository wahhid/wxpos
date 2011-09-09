import wx

import datetime
import os

from pos.modules.base.objects.idManager import ids

try:
    from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel
    can_view_pdf = True
except:
    can_view_pdf = False

class PDFReportPanel(wx.Panel):
    def _init_sizers(self):
        self.parametersSizer = wx.GridBagSizer(vgap=5)
        if self.show_date_range:
            self.parametersSizer.Add(self.fromLbl, (0, 0), border=20, flag=wx.RIGHT)
            self.parametersSizer.Add(self.fromDp, (0, 1), border=10, flag=wx.RIGHT)
            self.parametersSizer.Add(self.toLbl, (0, 2), border=10, flag=wx.RIGHT)
            self.parametersSizer.Add(self.toDp, (0, 3), border=10, flag=wx.RIGHT)

        for r, name in enumerate(self.field_order):
            f = self.fields[name]
            row = r+1 if self.show_date_range else r
            self.parametersSizer.Add(f['labelObj'], (row, 0), flag=wx.EXPAND | wx.ALL)
            self.parametersSizer.Add(f['fieldObj'], (row, 1), (1, 3), flag=f['style'])

        self.parametersSizer.AddGrowableCol(3, 1)

        self.parametersPanel.SetSizer(self.parametersSizer)
        self.parametersSizer.Fit(self.parametersPanel)

        self.viewSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.viewSizer.Add(self.pdfViewer, 1, flag=wx.EXPAND | wx.ALL)

        self.viewPanel.SetSizer(self.viewSizer)
        self.viewSizer.Fit(self.viewPanel)

        self.controlsSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlsSizer.Add(self.generateBtn, 0, border=10, flag=wx.RIGHT)# | wx.ALIGN_RIGHT)
        self.controlsSizer.Add(self.printBtn, 0, border=10, flag=wx.RIGHT)# | wx.ALIGN_RIGHT)

        self.controlsPanel.SetSizer(self.controlsSizer)
        self.controlsSizer.Fit(self.controlsPanel)

        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.Add(self.parametersPanel, 0, border=10, flag=wx.EXPAND | wx.ALL)
        self.mainSizer.Add(self.viewPanel, 1, border=10, flag=wx.EXPAND | wx.ALL)
        self.mainSizer.Add(self.controlsPanel, 0, border=10, flag=wx.ALIGN_RIGHT | wx.ALL)

        self.SetSizer(self.mainSizer)

    def _init_main(self):
        self.parametersPanel = wx.Panel(self, -1)
        self.viewPanel = wx.Panel(self, -1)
        self.controlsPanel = wx.Panel(self, -1)

        if self.show_date_range:
            self.fromLbl = wx.StaticText(self.parametersPanel, -1, label='Date Range')
            self.fromDp = wx.DatePickerCtrl(self.parametersPanel, -1, style=wx.DP_DROPDOWN)

            self.toLbl = wx.StaticText(self.parametersPanel, -1, label='To')
            self.toDp = wx.DatePickerCtrl(self.parametersPanel, -1, style=wx.DP_DROPDOWN | wx.DP_ALLOWNONE)
        
        self.generateBtn = wx.Button(self.controlsPanel, -1, label='Generate')
        self.generateBtn.Bind(wx.EVT_BUTTON, self.OnGenerateButton)

        self.printBtn = wx.Button(self.controlsPanel, -1, label='Print')
        self.printBtn.Bind(wx.EVT_BUTTON, self.OnPrintButton)

        if can_view_pdf:
            self.pdfViewer = pdfViewer(self.viewPanel, -1, wx.DefaultPosition, wx.DefaultSize, style=0)
        else:
            self.pdfViewer = wx.StaticText(self.viewPanel, -1, label='wxPython version 2.9 is required to preview pdf files.')

    def addParameter(self, label_text, wxObj, field_name, style=0):
        self.field_order.append(field_name)
        self.fields[field_name] = {}
        self.fields[field_name]['labelObj'] = wx.StaticText(self.parametersPanel, -1, label=label_text)
        self.fields[field_name]['fieldObj'] = wxObj
        self.fields[field_name]['style'] = style
        if self.validator is not None:
            self.fields[field_name]['fieldObj'].SetValidator(self.validator(self, field_name))
        self.parameters[field_name] = None
    
    def __init__(self, parent, validator=None, showDateRange=True):
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)

        self.show_date_range = showDateRange
        self.fields = {}
        self.field_order = []
        self.parameters = {}

        self._init_main()

        self.validator = validator
        if self.validator is not None:
            if self.show_date_range:
                pass
                #self.fromDp.SetValidator(self.validator('from_date'))
                #self.toDp.SetValidator(self.validator('to_date'))

    def _generateReport(self):
        self.parametersPanel.TransferDataFromWindow()
        parameters = self.parameters.copy()
        if self.show_date_range:
            wx_from_date = self.fromDp.GetValue()
            from_date = datetime.date.fromtimestamp(wx_from_date.GetTicks())
            
            wx_to_date = self.toDp.GetValue()
            to_date = None if not wx_to_date.IsValid() else datetime.date.fromtimestamp(wx_to_date.GetTicks())

        parameters.update({'from_date': from_date, 'to_date': to_date})

        filename = '../reports/%s.pdf' % (self.getFilename(**parameters),)
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

        if not self.parametersPanel.Validate():
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
