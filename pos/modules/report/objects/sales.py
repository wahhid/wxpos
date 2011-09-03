import pos

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
