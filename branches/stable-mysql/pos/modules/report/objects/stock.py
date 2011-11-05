import pos

import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, \
                                                 Paragraph, Spacer

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

from pos.modules.report.objects.pdf import PDFReport, stylesheet

import pos.modules.currency.objects.currency as currency

import pos.modules.stock.objects.product as product

class StockPDFReport(PDFReport):
    
    def _init_content(self):
        ps = product.find(list=True, in_stock=True)
    
        total = 0
        defc = currency.default
        headers = ('Reference', 'Name', 'Price', 'Quantity', 'Total')
        data = []
        marked = []
        for p in ps:
            reference = p.data['reference']
            name = p.data['name']
            price = p.data['price']
            pc = p.data['currency']
            quantity = p.data['quantity']
            
            data.append([reference,
                         name,
                         pc.format(price),
                         'x%d' % (quantity,),
                         pc.format(quantity*price)])
            if quantity<=0:
                marked.append(len(data))

            total += currency.convert(quantity*price, pc, defc)

        table = self.doTable(data=data, header=headers, marked_rows=marked)

        total_para = Paragraph('Total: %s' % (defc.format(total),),
                               stylesheet['Heading3Right'])
        self.elements.append(Spacer(36,36))
        self.elements.append(total_para)

def generateReport(filename):
    today = datetime.date.today()
    rep = StockPDFReport(filename, 'Stock Report',
                         None,
                         (today, None))

    return rep.build()
