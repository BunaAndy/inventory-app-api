import pyodbc
try:
    connstr = 'Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=master;Trusted_Connection=yes;'
    conn = pyodbc.connect(connstr, autocommit=True)
    cursor = conn.cursor()
except Exception as e:
    print('Could not connect to database: ', e)

try:
    query = 'CREATE DATABASE Inventory'
    result = cursor.execute(query)
    conn.commit()
except Exception as e:
    print(str(e))
    conn.rollback()
    raise Exception("Failed to execute query: " + str(e))

conn.close()
try:
    connstr = 'Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=Inventory;Trusted_Connection=yes;'
    conn = pyodbc.connect(connstr, autocommit=True)
    cursor = conn.cursor()
except Exception as e:
    print('Could not connect to database: ', e)

try:
    query = '''
    CREATE TABLE Project_Items (
        Barcode nvarchar(80),
        Name nvarchar(255),
        Quantity int,
        QuantityNeeded int,
        Catalog nvarchar(80),
        Manufacturer nvarchar(40)
    )
    '''
    result = cursor.execute(query)

    query = '''
    CREATE TABLE Projects (
        ProjectNumber nvarchar(10),
        ProjectName nvarchar(255),
        DateCreated date,
        BillOfMaterialsAdded bit
    )
    '''
    result = cursor.execute(query)

    query = '''
    CREATE TABLE All_Items (
        Barcode nvarchar(80),
        Name nvarchar(255),
        Catalog nvarchar(80),
        Manufacturer nvarchar(40)
    )
    '''
    result = cursor.execute(query)

    query = '''
    CREATE TABLE Users (
        Username nvarchar(20),
        PasswordHash nchar(16)
    )
    '''
    result = cursor.execute(query)
    
    query = '''
    CREATE TABLE Archived_Projects (
        ProjectNumber nvarchar(10),
        ProjectName nvarchar(255),
        DateCreated date,
        DateArchived date
    )
    '''
    result = cursor.execute(query)

except Exception as e:
    print(str(e))
    conn.rollback()
    raise Exception("Could not create Tables: " + str(e))