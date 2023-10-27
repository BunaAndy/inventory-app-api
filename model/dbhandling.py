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

# --------- PROJECT ITEMS ---------

# Get items from a specified project
def getProjectItems(projectID):
    query = 'SELECT * FROM Project_Items WHERE Project=?'
    with DBCursor() as cursor:
        out = makeEntryDicts(cursor.makeQuery(query, projectID), 'Project_Items')
    return out

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