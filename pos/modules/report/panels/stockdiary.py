import datetime

from .pdf import PDFReportPanel
import pos.modules.report.objects.stockdiary as stockdiary_report

class StockDiaryReportPanel(PDFReportPanel):
    def __init__(self, parent):
        PDFReportPanel.__init__(self, parent, showDateRange=True)

        self.parameters = {}

    def getFilename(self, from_date, to_date):
        today = datetime.date.today()
        return 'stockdiary-%s-%s' % (from_date, to_date)

    def generateReport(self, filename, from_date, to_date):
        return stockdiary_report.generateReport(filename, from_date, to_date)
