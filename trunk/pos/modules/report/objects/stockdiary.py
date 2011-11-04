import pos

import pos.modules.stock.objects.product as product

def getDiary(_from, _to):
    date_condition = "DATE(date) = DATE(%s)" if _to is None else "DATE(date)>=DATE(%s) AND DATE(date)<=DATE(%s)"
    sql = "SELECT id, operation, date, product_id, quantity FROM stockdiary WHERE " + \
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
    canvas.drawRightString(523, doc.bottomMargin+doc.height, "Stock Diary Report")

    canvas.setFont('Times-Roman',12)
    canvas.drawCentredString(doc.leftMargin+doc.width/2, doc.bottomMargin, "Page %d" % doc.page)
    #canvas.drawString(4 * inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()

def generateReport(filename, _from, _to):
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

    elements.append(Paragraph('Stock Diary Report', stylesheet['Title']))
    if _to is not None:
        elements.append(Paragraph('From %s To %s' % (_from, _to), stylesheet['Subtitle']))
    else:
        elements.append(Paragraph('On: %s' % (_from,), stylesheet['Subtitle']))

    lines = getDiary(_from, _to)
    
    headers = ('Operation ID', 'Operation', 'Date', 'Quantity', 'Product')
    data = [headers]
    for L in lines:
        oper_id, operation, date, p, quantity = L

        data.append([oper_id,
                     operation.title(),
                     date,
                     quantity,
                     p.data['name']])

    #colwidths = ['*']*4
    #colwidths = [float(PAGE_WIDTH)/len(headers)]*len(headers)
    table = Table(data=data,
                  #colWidths=colwidths,
                  style=TableStyle(
                    [('LINEBELOW', (0,0), (-1,0), 2, colors.green),
                     ('LINEABOVE', (0,2), (-1,-1), 0.25, colors.black)]
                ))

    elements.append(table)

    doc.build(elements, onFirstPage=framePage, onLaterPages=framePage)

    return doc
