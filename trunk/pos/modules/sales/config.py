import pos
from pos.menu import ModuleMenuBase, MenuRoot, MenuItem

dependencies = ('base', 'currency', 'user', 'stock', 'customer')

def load_database_objects():
    from pos.modules.sales.objects.ticket import Ticket
    from pos.modules.sales.objects.ticketline import TicketLine

def test_database_values():
    from pos.modules.sales.objects.ticket import Ticket
    from pos.modules.sales.objects.ticketline import TicketLine

    session = pos.database.session()

    from pos.modules.currency.objects.currency import Currency
    from pos.modules.user.objects.user import User
    from pos.modules.customer.objects.customer import Customer

    cu1 = session.query(Currency).filter_by(id=1).one()
    cu2 = session.query(Currency).filter_by(id=1).one()
    
    c1 = session.query(Customer).filter_by(id=1).one()
    
    u1 = session.query(User).filter_by(id=1).one()

    t1 = Ticket(cu1, u1, None, 'Test ticket 1')
    t2 = Ticket(cu2, None, c1, 'Test ticket 2')

    from pos.modules.stock.objects.product import Product
    
    p1 = session.query(Product).filter_by(id=1).one()

    tl1 = TicketLine('Ticketline 1-1', 2000, 1, False, t1, None)
    tl2 = TicketLine('Ticketline 1-2', 4500, 1, False, t1, None)
    tl3 = TicketLine('Ticketline 1-3 edited from p1', 5000, 2, True, t1, p1)
    tl4 = TicketLine('Ticketline 2-1', 5, 12, False, t2, None)
    tl5 = TicketLine('Ticketline 2-2 ewWeErRtTyYuUiIoOpP', 1.5, 12, True, t2, p1)

    [session.add(tl) for tl in (tl1, tl2, tl3, tl4, tl5)]
    session.commit()

def configDB(test=False):
    pos.db.query("""CREATE TABLE payment_methods (
         id int AUTO_INCREMENT PRIMARY KEY,
         name varchar(255) NOT NULL
    )""")

    pos.db.query("""INSERT INTO payment_methods (name) VALUES
        ('cash'), ('cheque'), ('voucher'), ('card'), ('free'), ('debt')
    """)

class ModuleMenu(ModuleMenuBase):
    def loadSubItems(self):
        from pos.modules.sales.panels import SalesPanel
        from pos.modules.sales.panels import DebtsPanel
        
        MenuItem(self.menu, "Main", "Sales", SalesPanel) #perm:sales
        MenuItem(self.menu, "Main", "Debts", DebtsPanel) #perm:sales
