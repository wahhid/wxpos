import pos

import datetime

import pos.modules.currency.objects.currency as currency

import pos.modules.stock.objects.product as product

def getProducts():
    return product.find(list=True, in_stock=True)

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, \
                                                 Paragraph, Spacer

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

def framePage(canvas,doc):
    canvas.saveState()

    canvas.setFont('Times-Italic',12)
    canvas.drawRightString(523, doc.bottomMargin+doc.height, "Stock Report")

    canvas.setFont('Times-Roman',12)
    canvas.drawCentredString(doc.leftMargin+doc.width/2, doc.bottomMargin, "Page %d" % doc.page)
    #canvas.drawString(4 * inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()

def generateReport(filename):
    doc = SimpleDocTemplate(filename)
    elements = []

    stylesheet = getSampleStyleSheet()
    stylesheet.add(ParagraphStyle(name='Heading3Right',
                            parent=stylesheet['Heading3'],
                            alignment=TA_RIGHT),
                   alias='h3-right')
    stylesheet.add(ParagraphStyle(name='Subtitle',
                            parent=stylesheet['Title'],
                            fontSize=14),
                   alias='subtitle')

    today = datetime.datetime.today()
    today = today.strftime('%Y-%m-%d %I:%M%p')
    elements.append(Paragraph('Stock Report', stylesheet['Title']))
    elements.append(Paragraph('On: %s' % (today,), stylesheet['Subtitle']))

    ps = getProducts()
    
    total = 0
    defc = currency.default
    headers = ('Reference', 'Name', 'Price', 'Quantity', 'Total')
    data = [headers]
    style = [('LINEBELOW', (0,0), (-1,0), 2, colors.green),
             ('ALIGN', (0,0), (-1,0), 'CENTER'),
             ('LINEABOVE', (0,2), (-1,-1), 0.25, colors.black),
             ('ALIGN', (1,1), (-1,-1), 'RIGHT')]
    for p in ps:
        reference = p.data['reference']
        name = p.data['name']
        price = p.data['price']
        pc = p.data['currency']
        quantity = p.data['quantity']

        if quantity<=0:
            style.append(('TEXTCOLOR', (0, len(data)), (-1, len(data)), colors.red))
        
        data.append([reference,
                     name,
                     pc.format(price),
                     'x%d' % (quantity,),
                     pc.format(quantity*price)])

        total += currency.convert(quantity*price, pc, defc)

    colwidths = ['17%']+['*']+['17%']*3
    #colwidths = [float(PAGE_WIDTH)/len(headers)]*len(headers)
    table = Table(data=data,
                  colWidths=colwidths,
                  style=TableStyle(style))
    elements.append(table)

    elements.append(Spacer(36,36))

    total_para = Paragraph('Stock Total: %s' % (defc.format(total),),
                           stylesheet['Heading3Right'])
    elements.append(total_para)

    doc.build(elements, onFirstPage=framePage, onLaterPages=framePage)

    return doc
