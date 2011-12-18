import pos

from sqlalchemy import func

from pos.modules.report.objects.pdf import TicketlistPDFReport

from pos.modules.sales.objects.ticket import Ticket

def getTickets(c, _from, _to, show):
    session = pos.database.session()
    query = session.query(Ticket).filter((Ticket.customer == c) & Ticket.payment_method.in_(show))
    if _to is None:
        query = query.filter(func.date(Ticket.date_close) == func.date(_from))
    else:
        query = query.filter(func.date(Ticket.date_close) >= func.date(_from) & func.date(Ticket.date_close) <= func.date(_to))
    query = query.order_by(Ticket.date_close.asc(), Ticket.date_open.asc(), Ticket.date_paid.desc())
    return query.all()

def generateReport(filename, c, _from, _to, show):
    rep = TicketlistPDFReport(filename, 'Customer Report',
                              'Customer: %s' % (c.name,),
                              (_from, _to),
                              tickets=getTickets(c, _from, _to, show))

    return rep.build()
