import pos

from pos.modules.report.objects.pdf import TicketlistPDFReport

import pos.modules.sales.objects.ticket as ticket

def getTickets(c, _from, _to, show):
    show = '(%s)' % (','.join(map(lambda s: "'"+s+"'", show)),)
    close_date_condition = "DATE(date_close) = DATE(%s)" if _to is None else "DATE(date_close)>=DATE(%s) AND DATE(date_close)<=DATE(%s)"
    sql = "SELECT id FROM tickets WHERE state>0 AND "+close_date_condition+" AND customer_id=%s" + \
            " AND payment_method IN %s" % (show,) + \
            " ORDER BY date_close ASC, date_open ASC, date_paid DESC"
    params = [_from.isoformat()]+([] if _to is None else [_to.isoformat()])+[c.id]
    cursor, success = pos.db.query(sql, params)
    if success:
        results = cursor.fetchall()
        return map(lambda r: ticket.find(_id=r[0]), results)
    else:
        return None

def generateReport(filename, c, _from, _to, show):
    ts = getTickets(c, _from, _to, show)
    
    rep = TicketlistPDFReport(filename, 'Customer Report',
                              'Customer: %s' % (c.data['name'],),
                              (_from, _to),
                              tickets=ts)

    return rep.build()
