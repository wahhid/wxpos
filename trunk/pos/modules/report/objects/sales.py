import pos

from pos.modules.report.objects.pdf import TicketlistPDFReport

import pos.modules.sales.objects.ticket as ticket

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

def generateReport(filename, _from, _to):
    ts = getTickets(_from, _to)
    
    rep = TicketlistPDFReport(filename, 'Sales Report',
                              None,
                              (_from, _to),
                              tickets=ts)

    return rep.build()
