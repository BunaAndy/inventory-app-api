import model.dbhandling as db
from controller.functions.get_functions import *

# Return item in db
def addProjectItems(items, projectNumber):
    # Check that project exists before querying
    try:
        proj = db.getItem(projectNumber)
    except Exception as e:
        print(e)
        return {
            'error': 'Get Project Error', 
            'message':'Error finding project ' + str(projectNumber) + ': ' + str(e)}, 500
    
    # Add new Items
    try:
        db.addProjectItems(items)
    except Exception as e:
        print(e)
        return {
            'error': 'Adding Items Error', 
            'message':'Error adding items to project : ' + str(projectNumber) + ', ' + str(e)}, 500
    # Update Items
    try:
        itemCols = db.updateProjectItems(items)
    except Exception as e:
        print(e)
        return {
            'error': 'Get Columns Error', 
            'message':'Error updating items in project : ' + str(projectNumber) + ', ' + str(e)}, 500

    # Creates json with output data
    response = getProjectItems(projectNumber)
    return response