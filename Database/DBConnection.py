import mysql.connector

class Connector :
    def __init__(self):
        self.conn = mysql.connector.connect (
            host = '127.0.0.1',
            user = 'root',
            password = 'Mm.261005',
            database = 'FirmSystem'
        )

        self.cursor = self.conn.cursor()

    def get_connec(self) :
        return self.conn
    
    def get_cursor(self) :
        return self.cursor
    
    def close_connec(self) :
        if self.conn :
            self.conn.close()

        if self.cursor :
            self.cursor.close()