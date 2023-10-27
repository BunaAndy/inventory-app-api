import pyodbc
import hashlib
import re
import datetime
from model.connection import DBCursor

# --------- ALL ITEMS ---------

# Get specific item based on Barcode
def getItem(barcode):
    query = 'SELECT * FROM All_Items WHERE Barcode = ?'
    with DBCursor() as cursor:
        item = makeEntryDicts(cursor.makeQuery(query, barcode), 'All_Items')
    return item

# Get all item info saved in DB
def getAllItems():
    query = 'SELECT * FROM All_Items'
    with DBCursor() as cursor:
        items = makeEntryDicts(cursor.makeQuery(query), 'All_Items')
    return items

def addItems(items):
    params = []
    for item in items:
        params.append(
            # First, ensure item does not exist
            (item['Barcode'],
             item['Name'],
             item['Catalog'],
            # Then if it does not, add the item to the db
             item['Barcode'],
             item['Name'],
             item['Catalog']))

    query = f'''
    IF NOT EXISTS (SELECT 1 FROM Project_Items WHERE Barcode = ? OR Name = ? OR Catalog = ?)  
    BEGIN  
        INSERT INTO Project_Items values (?, ?, ?);
    END '''

    with DBCursor() as cursor:
        cursor.makeManyQueries(query, params)
    return

def updateItems(items):
    params = []
    for item in items:
        params.append(
            # First, ensure item exists
            (item['Barcode'],
             item['Name'],
             item['Catalog'],
            # Then if it does, update the values
             item['Barcode'],
             item['Name'],
             item['Catalog'],
            # Where they match the criteria
             item['Barcode'],
             item['Name'],
             item['Catalog']))

    query = f'''
    IF EXISTS (SELECT 1 FROM Project_Items WHERE Barcode = ? OR Name = ? OR Catalog = ?)  
    BEGIN  
        UPDATE Project_Items  
        SET Barcode = ?,
        Name = ?,
        Catalog = ?
        WHERE (Barcode = ? OR Name = ? OR Catalog = ?);
    END '''

    with DBCursor() as cursor:
        cursor.makeManyQueries(query, params)
    return

# --------- PROJECT ITEMS ---------

# Get items from a specified project
def getProjectItems(projectID):
    query = 'SELECT * FROM Project_Items WHERE Project=?'
    with DBCursor() as cursor:
        out = makeEntryDicts(cursor.makeQuery(query, projectID), 'Project_Items')
    return out

def addProjectItems(items):
    params = []
    for item in items:
        params.append(
            # First, ensure item does not exist
            (item['Barcode'],
             item['Name'],
             item['Catalog'],
             item['Project'],
            # Then if it does not, add the item to the db
             item['Barcode'],
             item['Name'],
             item['Project'],
             item['Quantity'],
             item['Quantity Needed'],
             item['Catalog']))

    query = f'''
    IF NOT EXISTS (SELECT 1 FROM Project_Items WHERE (Barcode = ? OR Name = ? OR Catalog = ?) AND Project = ?)  
    BEGIN  
        INSERT INTO Project_Items values (?, ?, ?, ?, ?);
    END '''

    with DBCursor() as cursor:
        cursor.makeManyQueries(query, params)
    return

def updateProjectItems(items):
    params = []
    for item in items:
        params.append(
            # First, ensure item exists
            (item['Barcode'],
             item['Name'],
             item['Catalog'],
             item['Project'],
            # Then if it does, update the quantities
             item['Quantity'],
             item['Quantity Needed'],
            # Where the it matches the criteria 
             item['Barcode'],
             item['Name'],
             item['Catalog'],
             item['Project']))

    query = f'''
    IF EXISTS (SELECT 1 FROM Project_Items WHERE (Barcode = ? OR Name = ? OR Catalog = ?) AND Project = ?)  
    BEGIN  
        UPDATE Project_Items  
        SET Quantity = Quantity + ?,
        Quantity_Needed = ?
        WHERE (Barcode = ? OR Name = ? OR Catalog = ?)
        AND Project = ?;
    END '''

    with DBCursor() as cursor:
        cursor.makeManyQueries(query, params)
    return

# --------- PROJECTS ---------

# Get information on a singular project
def getProject(projectID):
    query = 'SELECT * FROM Projects WHERE ProjectNumber=?'
    with DBCursor() as cursor:
        out = makeEntryDicts(cursor.makeQuery(query, projectID), 'Projects')
    return out

# Get all Projects defined in the DB
def getAllProjects():
    query = 'SELECT * FROM Projects'
    with DBCursor() as cursor:
        projs = makeEntryDicts(cursor.makeQuery(query), 'Projects')
    out = []
    for proj in projs:
        proj["Date Created"] = str(proj["Date Created"].strftime("%a, %d %b %Y"))
        out.append(proj)
    return out

# --------- USERS/AUTH ---------

# Get a specified user in the database
def getUser(username):
    query = 'SELECT * FROM Users WHERE Username=?'
    with DBCursor() as cursor:
        users = cursor.makeQuery(query, username)
    return users

# --------- UTIL ---------

# Gets columns of accessed table in a nicer list of string format with added
# spaces instead of using the keys in entry dicts
def getColumns(table):
    query = 'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?'
    with DBCursor() as cursor:
        cols = cursor.makeQuery(query, table)
    out = []
    for col in cols:
        colName = re.sub(r'(\w)([A-Z])', r'\1 \2', col[0]).replace('_', '')
        out.append(colName)
    return out

# Util function to "prettify" all entries, creating dicts for json transfer
# and using formatted column names
def makeEntryDicts(entries, table):
    newEntries = []
    cols = getColumns(table)
    for entry in entries:
        entryDict = {}
        for index, col in enumerate(cols):
            val = entry[index]
            if (val == None):
                val = ''
            entryDict[col] = val
        newEntries.append(entryDict.copy())
    return newEntries