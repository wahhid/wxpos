from .pdf import PDFReportPanel
import pos.modules.report.objects.sales as sales_report

class SalesReportPanel(PDFReportPanel):
    def __init__(self, parent):
        PDFReportPanel.__init__(self, parent, showDateRange=True)

    def getFilename(self, from_date, to_date):
        return 'sales-%s-%s' % (from_date, to_date)

    def generateReport(self, filename, from_date, to_date):
        return sales_report.generateReport(filename, from_date, to_date)
