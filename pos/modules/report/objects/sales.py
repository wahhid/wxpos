import pos

from sqlalchemy import func

from pos.modules.report.objects.pdf import TicketlistPDFReport

from pos.modules.sales.objects.ticket import Ticket

def getTickets(_from, _to=None):
    session = pos.database.session()
    query = session.query(Ticket)
    if _to is None:
        query = query.filter(func.date(Ticket.date_close) == func.date(_from))
    else:
        query = query.filter(func.date(Ticket.date_close) >= func.date(_from) & func.date(Ticket.date_close) <= func.date(_to))
    query = query.order_by(Ticket.date_close.asc(), Ticket.date_open.asc(), Ticket.date_paid.desc())
    return query.all()

def generateReport(filename, _from, _to):
    rep = TicketlistPDFReport(filename, 'Sales Report',
                              None,
                              (_from, _to),
                              tickets=getTickets(_from, _to))

    return rep.build()
