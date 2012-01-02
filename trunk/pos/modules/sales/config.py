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
    cu2 = session.query(Currency).filter_by(id=2).one()
    
    c1 = session.query(Customer).filter_by(id=1).one()
    
    u1 = session.query(User).filter_by(id=1).one()

    t1 = Ticket(discount=0, currency=cu1, user=u1, customer=None, comment='Test ticket 1')
    t2 = Ticket(discount=0.3, currency=cu2, user=u1, customer=c1, comment='Test ticket 2')

    from pos.modules.stock.objects.product import Product
    
    p1 = session.query(Product).filter_by(id=1).one()

    tl1 = TicketLine(description='Ticketline 1-1', sell_price=2000, amount=1, discount=0, is_edited=False, ticket=t1, product=None)
    tl2 = TicketLine(description='Ticketline 1-2', sell_price=4500, amount=1, discount=0, is_edited=False, ticket=t1, product=None)
    tl3 = TicketLine(description='Ticketline 1-3 edited from p1', sell_price=5000, amount=2, discount=0, is_edited=True, ticket=t1, product=p1)
    tl4 = TicketLine(description='Ticketline 2-1', sell_price=5, amount=12, discount=0, is_edited=False, ticket=t2, product=None)
    tl5 = TicketLine(description='Ticketline 2-2 ewWeErRtTyYuUiIoOpP', sell_price=1.5, amount=12, discount=0, is_edited=True, ticket=t2, product=p1)

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
