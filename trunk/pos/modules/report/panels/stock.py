import datetime

from .pdf import PDFReportPanel
import pos.modules.report.objects.stock as stock_report

class StockReportPanel(PDFReportPanel):
    def __init__(self, parent):
        PDFReportPanel.__init__(self, parent, showDateRange=False)

        self.parameters = {}

    def getFilename(self):
        today = datetime.date.today()
        return 'stock-%s' % (today,)

    def generateReport(self, filename):
        return stock_report.generateReport(filename)
