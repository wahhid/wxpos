class TicketlineDB:
    def getAllTicketlines(self):
        sql = "SELECT id FROM ticketlines"
        params = None
        cursor, success = self.db.query('getAllTicketlines', sql, params)
        if success:
            results = cursor.fetchall()
            return map(lambda r: r[0], results)
        else:
            return None

    def insertTicketline(self, description, sell_price, amount, ticket_id, product_id, is_edited):
        sql = """INSERT INTO ticketlines
            (description, sell_price, amount, ticket_id, product_id, is_edited)
        VALUES (%s, %s, %s, %s, %s, %s)
"""
        params = (description, sell_price, amount, ticket_id, product_id, is_edited)
        cursor, success = self.db.query('insertTicketline', sql, params)
        if success:
            ticketline_id = self.conn.insert_id()
            return ticketline_id
        else:
            return None

    def updateTicketline(self, ticketline_id, description=None, sell_price=None,
                         amount=None, ticket_id=None, product_id=None, is_edited=None):
        fields = ('description', 'sell_price', 'amount', 'ticket_id', 'product_id', 'is_edited')
        update_str = [f+"=%s" for f in fields if locals()[f] is not None]
        if len(update_str) == 0: return None
        
        sql = "UPDATE ticketlines SET "+",".join(update_str)+" WHERE id=%s"
        params = [locals()[f] for f in fields if locals()[f] is not None]
        params.append(ticketline_id)
        cursor, success = self.db.query('updateTicketline', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None

    def deleteTicketline(self, ticketline_id):
        sql = "DELETE FROM ticketlines WHERE id=%s"
        params = (ticketline_id,)
        cursor, success = self.db.query('deleteTicketline', sql, params)
        if success:
            return (cursor.rowcount == 1)
        else:
            return None
    
    def getTicketlineInfo(self, ticketline_id):
        sql = """SELECT description, sell_price, amount,
                        ticket_id, product_id, is_edited
                FROM ticketlines WHERE id=%s
"""
        params = (ticketline_id,)
        cursor, success = self.db.query('getTicketlineInfo', sql, params)
        if success:
            results = cursor.fetchone()
            if len(results)>0:
                return results
            else:
                return None
        else:
            return None
