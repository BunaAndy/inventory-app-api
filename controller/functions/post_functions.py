import model.dbhandling as db
from controller.functions.get_functions import *

# Return item in db
def addProjectItems(items, projectNumber):
    # Check that project exists before querying
    try:
        projs = db.getProject(projectNumber)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Get Project Error', 
            'message':'Error finding project ' + str(projectNumber) + ': ' + str(e)}, 500

    if len(projs) == 0:
        return {
            'error': 'Project not Found', 
            'message':'No project with number: ' + str(projectNumber) + ' found'}, 404

    # Add new Items to all Items
    try:
        db.addItems(items)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Adding Items Error', 
            'message':'Error adding items to all items : ' + str(e)}, 500
    
    # Add new Project Items
    try:
        db.addProjectItems(items, projectNumber)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Adding Items Error', 
            'message':'Error adding items to project : ' + str(projectNumber) + ', ' + str(e)}, 500

    response = {'success': True}, 200
    return response

def incrementProjectItems(items, projectNumber):
    # Check that project exists before querying
    try:
        projs = db.getProject(projectNumber)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Get Project Error', 
            'message':'Error finding project ' + str(projectNumber) + ': ' + str(e)}, 500

    if len(projs) == 0:
        return {
            'error': 'Project not Found', 
            'message':'No project with number: ' + str(projectNumber) + ' found'}, 404
    
    # Update Items
    try:
        db.incrementProjectItemQuantities(items, projectNumber)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Update Items Error', 
            'message':'Error updating items in project : ' + str(projectNumber) + ', ' + str(e)}, 500

    response = {'success': True}, 200
    return response

def addProject(projectNumber, projectName):
    try:
        db.addProject(projectNumber, projectName)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Update Items Error', 
            'message':'Error updating items in project : ' + str(projectNumber) + ', ' + str(e)}, 500
    response = {'success': True}, 200
    return response

def modifyProjectItems(items, projectNumber):
    # Check that project exists before querying
    try:
        projs = db.getProject(projectNumber)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Get Project Error', 
            'message':'Error finding project ' + str(projectNumber) + ': ' + str(e)}, 500

    if len(projs) == 0:
        return {
            'error': 'Project not Found', 
            'message':'No project with number: ' + str(projectNumber) + ' found'}, 404
    
    # Update Items
    try:
        db.updateProjectItems(items, projectNumber)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Update Items Error', 
            'message':'Error updating items in project : ' + str(projectNumber) + ', ' + str(e)}, 500

    response = {'success': True}, 200
    return response

def deleteProjectItems(items, projectNumber):
    try:
        projs = db.getProject(projectNumber)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Get Project Error', 
            'message':'Error finding project ' + str(projectNumber) + ': ' + str(e)}, 500

    if len(projs) == 0:
        return {
            'error': 'Project not Found', 
            'message':'No project with number: ' + str(projectNumber) + ' found'}, 404
    
    # Delete Items
    try:
        db.removeProjectItems(items, projectNumber)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Delete Items Error', 
            'message':'Error deleting items in project : ' + str(projectNumber) + ', ' + str(e)}, 500
    
    response = {'success': True}, 200
    return response

def modifyItems(items):
    # Update Items
    try:
        db.updateItems(items)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Update Items Error', 
            'message':'Error deleting items: ' + str(e)}, 500

    response = {'success': True}, 200
    return response

def deleteItems(items):
    # Delete Items
    try:
        db.removeItems(items)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Delete Items Error', 
            'message':'Error deleting items: ' + str(e)}, 500
    
    response = {'success': True}, 200
    return response