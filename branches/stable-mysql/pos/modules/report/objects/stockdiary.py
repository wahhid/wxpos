import pos

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, \
                                                 Paragraph, Spacer

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

from pos.modules.report.objects.pdf import PDFReport, stylesheet

import pos.modules.stock.objects.product as product

def getDiary(_from, _to):
    date_condition = "DATE(date) = DATE(%s)" if _to is None else "DATE(date)>=DATE(%s) AND DATE(date)<=DATE(%s)"
    sql = "SELECT id, date, operation, product_id, quantity FROM stockdiary WHERE " + \
            date_condition + \
            " ORDER BY date ASC"
    params = [_from.isoformat()]+([] if _to is None else [_to.isoformat()])
    cursor, success = pos.db.query(sql, params)
    if success:
        results = cursor.fetchall()
        def process(r):
            r = list(r)
            r[3] = product.find(_id=r[3])
            return r
        return map(process, results)
    else:
        return None

class StockDiaryPDFReport(PDFReport):
    
    def _init_content(self):
        lines = getDiary(*self.date_range)
    
        headers = ('Operation ID', 'Date', 'Operation', 'Quantity', 'Product')
        data = []
        for L in lines:
            oper_id, date, operation, p, quantity = L

            data.append([oper_id,
                         date,
                         operation.title(),
                         quantity,
                         p.data['name']])

        table = self.doTable(data=data, header=headers)

def generateReport(filename, _from, _to):
    rep = StockDiaryPDFReport(filename, 'Stock Diary Report',
                         None,
                         (_from, _to))

    return rep.build()
