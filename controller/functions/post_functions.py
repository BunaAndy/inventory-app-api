import model.dbhandling as db
from controller.functions.get_functions import *

# Return item in db
def addProjectItems(items, projectNumber):
    # Check that project exists before querying
    try:
        projs = db.getProject(projectNumber)
    except Exception as e:
        print(e)
        return {
            'error': 'Get Project Error', 
            'message':'Error finding project ' + str(projectNumber) + ': ' + str(e)}, 500
    if len(projs) == 0:
        return {
            'error': 'Project not Found', 
            'message':'No project with number: ' + str(projectNumber) + ' found'}, 404
    
    # Add new Items
    try:
        db.addProjectItems(items, projectNumber)
    except Exception as e:
        print(e)
        return {
            'error': 'Adding Items Error', 
            'message':'Error adding items to project : ' + str(projectNumber) + ', ' + str(e)}, 500
    
    # Update Items
    try:
        db.updateProjectItems(items, projectNumber)
    except Exception as e:
        print(e)
        return {
            'error': 'Update Items Error', 
            'message':'Error updating items in project : ' + str(projectNumber) + ', ' + str(e)}, 500

    # Creates json with output data
    response = getProjectItems(projectNumber)
    return response