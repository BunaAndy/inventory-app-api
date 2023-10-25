import pyodbc
from connection_string import connection_string as conStr

class DBCursor():
    def __init__(self):
        try:
            self.conn = pyodbc.connect(conStr)
            self.conn.autocommit = False
        except Exception as e:
            raise Exception('Could not open connection to database')

    def __enter__(self):
        self.curs = self.conn.cursor()
        return self

    def __exit__(self):
        self.conn.commit()
        self.curs.close()

    def makeQuery(self, query, *args):
        try: 
            result = self.curs.execute(query, *args)
        except pyodbc.DatabaseError as e:
            self.conn.rollback()
            raise Exception("Failed to execute query: " + e)
        out = []
        try:
            out = result.fetchall()
        except Exception as e:
            out = []
        self.conn.commit()
        return out
    
    def makeManyQueries(self, query, params):
        out = []
        try:
            self.curs.executemany(query, params)
        except pyodbc.DatabaseError as e:
            self.conn.rollback()
            raise Exception("Failed to execute query: " + e)
        self.conn.commit()
        return []