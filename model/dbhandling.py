import pyodbc
import hashlib
import re
import datetime
from connection import DBCursor

# Returns columns of accessed table in a nicer list of string format with added
# spaces instead of using the keys in entry dicts
def getColumns(table):
    query = 'select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = ?'
    with DBCursor() as cursor:
        cols = cursor.makeQuery(query, table)
    out = []
    for col in cols:
        colName = re.sub(r'(\w)([A-Z])', r'\1 \2', col[0]).replace('_', '')
        out.append(colName)
    return out

# Get all Projects defined in the DB
def getAllProjects():
    query = 'select * from Projects'
    with DBCursor() as cursor:
        projs = makeEntryDicts(cursor.makeQuery(query), 'Projects')
    out = []
    for proj in projs:
        proj["Date Created"] = str(proj["Date Created"].strftime("%a, %d %b %Y"))#datetime.datetime.strptime(proj["Date Created"], "%a, %d %b %Y, %H:%M:%S %Z").date()
        out.append(proj)
    return out

def getAllItems():
    query = 'select * from All_Items'
    with DBCursor() as cursor:
        items = makeEntryDicts(cursor.makeQuery(query), 'All_Items')
    return items

def getItem(barcode):
    query = 'select * from All_Items where Barcode = ?'
    with DBCursor() as cursor:
        item = makeEntryDicts(cursor.makeQuery(query, barcode), 'All_Items')
    return item

def getProject(projectID):
    query = 'select * from Project_Items where Project=?'
    with DBCursor() as cursor:
        out = makeEntryDicts(cursor.makeQuery(query, projectID), 'Project_Items')
    return out

# Util function to "prettify" all entries, creating dicts for json transfer
# and using formatted column names
def makeEntryDicts(entries, table):
    newEntries = []
    cols = getColumns(table)
    for entry in entries:
        entryDict = {}
        for index, col in enumerate(cols):
            entryDict[col] = entry[index]
        newEntries.append(entryDict.copy())
    return newEntries