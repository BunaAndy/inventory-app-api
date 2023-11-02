import pyodbc
from model.connection_string import connection_string as conStr

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

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            print(exc_type, exc_value, tb)
        self.conn.commit()
        self.curs.close()
        return True

    def makeQuery(self, query, *args):
        try: 
            result = self.curs.execute(query, *args)
        except Exception as e:
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
        except Exception as e:
            self.conn.rollback()
            raise Exception("Failed to execute queries: " + e)
        self.conn.commit()
        return []