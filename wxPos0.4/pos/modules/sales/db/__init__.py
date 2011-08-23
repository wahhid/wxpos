from .ticket import TicketDB
from .ticketline import TicketlineDB

from pos.db.subset import DBSubset

class ModuleDB(DBSubset, TicketDB, TicketlineDB):
    pass

def config(db):
    db.createTable("tickets", """
         id int AUTO_INCREMENT PRIMARY KEY,
         comment varchar(255) DEFAULT NULL,
         date_open DATETIME DEFAULT NULL,
         date_close DATETIME DEFAULT NULL,
         user_id int NOT NULL,
         state int NOT NULL DEFAULT 1,
         FOREIGN KEY (user_id) REFERENCES users(id)
    """)
    
    db.createTable("ticketlines", """
         id int AUTO_INCREMENT PRIMARY KEY,
         description varchar(255) NOT NULL,
         sell_price double NOT NULL,
         amount int NOT NULL DEFAULT 1,
         ticket_id  int NOT NULL,
         product_id int DEFAULT NULL,
         is_edited bool DEFAULT 0,
         FOREIGN KEY (ticket_id) REFERENCES tickets(id)
    """)
