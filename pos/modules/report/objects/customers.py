import pos

import pos.modules.currency.objects.currency as currency

import pos.modules.sales.objects.ticket as ticket
import pos.modules.sales.objects.ticketline as ticketline

def getTickets(_from, _to=None):
    if _to is None:
        sql = "SELECT id FROM tickets WHERE state>0 AND DATE(date_close) = DATE(%s)"
        params = (_from.isoformat(),)
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: ticket.find(_id=r[0]), results)
        else:
            return None
    else:
        sql = "SELECT id FROM tickets WHERE state>0 AND DATE(date_close)>=DATE(%s) AND DATE(date_close)<=DATE(%s)"
        params = (_from.isoformat(), _to.isoformat())
        cursor, success = pos.db.query(sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: ticket.find(_id=r[0]), results)
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
    canvas.drawRightString(523, doc.bottomMargin+doc.height, "Sales Report")

    canvas.setFont('Times-Roman',12)
    canvas.drawCentredString(doc.leftMargin+doc.width/2, doc.bottomMargin, "Page %d" % doc.page)
    #canvas.drawString(4 * inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()

def generateReport(filename, c, _from, _to):
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

    elements.append(Paragraph('Customer Report', stylesheet['Title']))
    elements.append(Paragraph(c.data['name'], stylesheet['Subtitle']))
    if _to is not None:
        elements.append(Paragraph('From %s To %s' % (_from, _to), stylesheet['Subtitle']))
    else:
        elements.append(Paragraph('On: %s' % (_from,), stylesheet['Subtitle']))

    ts = filter(lambda t: t.data["customer"] == c, getTickets(_from, _to))
    
    period_total = 0
    defc = currency.default
    headers = ('Description', 'Price', 'Amount', 'Total')
    for t in ts:
        tls = ticketline.find(list=True, ticket=t)
        
        elements.append(Spacer(18,18))

        row = [Paragraph('Ticket #%.3d' % (t.id,), stylesheet['Heading3']),
               Paragraph(str(t.data['date_close']), stylesheet['Heading3Right'])]
        info_table = Table(
                      data=[row],
                      colWidths=[doc.width/2.0]*2
                      )
        elements.append(info_table)

        data = [headers]
        tc = t.data['currency']
        total = 0
        for tl in tls:
            description = tl.data['description']
            sell_price = tl.data['sell_price']
            amount = tl.data['amount']
            data.append([description,
                         tc.format(sell_price),
                         'x%d' % (amount,),
                         tc.format(amount*sell_price)])

            total += tl.data['amount']*tl.data['sell_price']
        data.append(['', '', 'Sub Total', tc.format(total)])
        period_total += currency.convert(total, tc, defc)

        colwidths = ['*']+['17%']*3
        #colwidths = [float(PAGE_WIDTH)/len(headers)]*len(headers)
        table = Table(data=data,
                      colWidths=colwidths,
                      style=TableStyle(
                        [('LINEBELOW', (0,0), (-1,0), 2, colors.green),
                         ('ALIGN', (0,0), (-1,0), 'CENTER'),
                         ('LINEABOVE', (0,2), (-1,-1), 0.25, colors.black),
                         ('LINEBELOW', (0,-2), (-1,-2), 2, colors.green),
                         ('ALIGN', (1,1), (-1,-1), 'RIGHT')]
                    ))

        elements.append(table)

    elements.append(Spacer(36,36))

    total_para = Paragraph('Total Due: %s' % (defc.format(period_total),),
                           stylesheet['Heading3Right'])
    elements.append(total_para)

    doc.build(elements, onFirstPage=framePage, onLaterPages=framePage)

    return doc
