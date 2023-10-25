import model.dbhandling as db
from flask import jsonify

# Return item in db
def getItem(barcode):
    # Check that project exists before querying
    try:
        item = db.getItem(barcode)
    except Exception as e:
        print(e)
        return jsonify({
            'error': 'Get Project Error', 
            'message':'Error fetching item ' + str(barcode) + ': ' + str(e)}), 500
    
    try:
        itemCols = db.getColumns('All_Items')
    except Exception as e:
        print(e)
        return jsonify({
            'error': 'Get Columns Error', 
            'message':'Error fetching columns of All Items: ' + str(e)}), 500

    # Creates json with output data
    response = jsonify({
        'entries': item,
        'projectNumber': 'Item',
        'projectName': 'Item',
        'columns': itemCols,
        'success': True})
    return response, 200

# Return all items in db
def getItems():
    try:
        items = db.getAllItems()
    except Exception as e:
        print(e)
        return jsonify({
            'error': 'Get All Items Error', 
            'message':'Error fetching all items: ' + str(e)}), 500
    
    try:
        allItemsCols = db.getColumns('All_Items')
    except Exception as e:
        print(e)
        return jsonify({
            'error': 'Get Columns Error', 
            'message':'Error fetching columns of all items: ' + str(e)}), 500

    # Creates json with output data
    response = jsonify({
        'entries': items,
        'projectNumber': 'All Items',
        'projectName': 'All Items',
        'columns': allItemsCols,
        'success': True})
    return response, 200

# Return all items in project in db
def getProjectItems(projectNumber):
    # Check that project exists before querying
    try:
        projects = db.getProject(projectNumber)
    except Exception as e:
        print(e)
        return jsonify({
            'error': 'Get Project Error', 
            'message':'Error fetching project ' + str(projectNumber) + ': ' + str(e)}), 500
    if len(projects) == 0:
        return jsonify({
            'error': 'JSON Error', 
            'message':'No project with name: ' + str(projectNumber) + ' found'}), 400
    
    project = projects[0]
    try:
        projectData = db.getProjectItems(projectNumber)
    except Exception as e:
        print(e)
        return jsonify({
            'error': 'Get Project Items Error', 
            'message':'Error fetching project items in project ' + str(projectNumber) + ': ' + str(e)}), 500
    
    project = projects[0]
    try:
        projectCols = db.getColumns('Project_Items')
    except Exception as e:
        print(e)
        return jsonify({
            'error': 'Get Columns Error', 
            'message':'Error fetching columns of project items: ' + str(e)}), 500

    projectName = project['Project Name']

    # Creates json with output data
    response = jsonify({
        'entries': projectData,
        'projectNumber': projectNumber,
        'projectName': projectName,
        'columns': projectCols,
        'success': True})
    return response, 200

# Return specified project in db
def getProject(projectNumber):
    try:
        projects = db.getProject(projectNumber)
    except Exception as e:
        print(e)
        return jsonify({
            'error': 'Get Project Error', 
            'message':'Error fetching project ' + str(projectNumber) + ': ' + str(e)}), 500 

    try:
        projectCols = db.getColumns('Projects')
    except Exception as e:
        print(e)
        return jsonify({
            'error': 'Get Columns Error',
            'message':'Error fetching columns of projects' + ': ' + str(e)}), 500

    response = jsonify({
        'entries': projects, 
        'projectNumber': 'All Projects', 
        'projectName': 'All Projects', 
        'columns': projectCols, 
        'success': True})
    return response, 200

# Return projects in db
def getProjects():
    try:
        projects = db.getAllProjects()
    except Exception as e:
        print(e)
        return jsonify({
            'error': 'Get Projects Error',
            'message':'Error fetching all projects: ' + str(e)}), 500  

    try:
        projectCols = db.getColumns('Projects')
    except Exception as e:
        print(e)
        return jsonify({
            'error': 'Get Columns Error',
            'message':'Error fetching columns of projects' + ': ' + str(e)}), 500

    response = jsonify({
        'entries': projects, 
        'projectNumber': 'All Projects', 
        'projectName': 'All Projects', 
        'columns': projectCols, 
        'success': True})
    return response, 200