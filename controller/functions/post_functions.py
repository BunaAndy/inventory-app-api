import model.dbhandling as db
from controller.functions.get_functions import *
import hashlib
import jwt
import os


# --------- PROJECT ITEMS ---------

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
        db.updatePIQuantity(items, projectNumber)
        db.updatePIQuantityNeeded(items, projectNumber)
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

def pullFromStock(items, projectNumber):
    try:
        projs = db.getProject(projectNumber)
    except Exception as e:
        return {
            'error': 'Get Project Error', 
            'message':'Error finding project ' + str(projectNumber) + ': ' + str(e)}, 500

    if len(projs) == 0:
        return {
            'error': 'Project not Found', 
            'message':'No project with number: ' + str(projectNumber) + ' found'}, 404
    
    # Pull Items
    try:
        db.pullStock(items)
    except Exception as e:
        return {
            'error': 'Delete Items Error', 
            'message':'Error deleting items in project : ' + str(projectNumber) + ', ' + str(e)}, 500
    
    # Pull Items
    try:
        db.incrementProjectItemQuantities(items, projectNumber)
    except Exception as e:
        return {
            'error': 'Pull Items Error', 
            'message':'Error pulling items into project : ' + str(projectNumber) + ', ' + str(e)}, 500
    
    response = {'success': True}, 200
    return response

def uploadBOM(items, projectNumber):
    try:
        projs = db.getProject(projectNumber)
    except Exception as e:
        return {
            'error': 'Get Project Error', 
            'message':'Error finding project ' + str(projectNumber) + ': ' + str(e)}, 500
    if len(projs) == 0:
        return {
            'error': 'Project not Found', 
            'message':'No project with number: ' + str(projectNumber) + ' found'}, 404
    project = projs[0]

    if project['Bill Of Materials Added']:
        return {
            'error': 'Cannot Reupload BOM', 
            'message':'Project already has BOM, try using Reupload endpoint after logging in'}, 401

    project['Bill Of Materials Added'] = True

    try:
        db.updatePIQuantityNeeded(items, projectNumber)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Update Items Error', 
            'message':'Error updating items in project : ' + str(projectNumber) + ', ' + str(e)}, 500

    addProjectItems(items, projectNumber)
    modifyProjects([project])

    response = {'success': True}, 200
    return response

def reuploadBOM(items, projectNumber):
    try:
        projs = db.getProject(projectNumber)
    except Exception as e:
        return {
            'error': 'Get Project Error', 
            'message':'Error finding project ' + str(projectNumber) + ': ' + str(e)}, 500
    if len(projs) == 0:
        return {
            'error': 'Project not Found', 
            'message':'No project with number: ' + str(projectNumber) + ' found'}, 404
    project = projs[0]

    try:
        db.updatePIQuantityNeeded(items, projectNumber)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Update Items Error', 
            'message':'Error updating items in project : ' + str(projectNumber) + ', ' + str(e)}, 500

    addProjectItems(items, projectNumber)

    response = {'success': True}, 200
    return response

# --------- PROJECTS ---------

def addProject(projectNumber, projectName):
    try:
        db.addProject(projectNumber, projectName)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Add Project Error', 
            'message':'Error adding project : ' + str(projectNumber) + ', ' + str(e)}, 500
    response = {'success': True}, 200
    return response

def modifyProjects(items):
    try:
        db.updateProjects(items)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Update Projects Error', 
            'message':'Error updating projects : ' + str(e)}, 500
    response = {'success': True}, 200
    return response

def deleteProjects(items):
    try:
        db.removeProjects(items)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Delete Projects Error', 
            'message':'Error deleting projects : ' + str(e)}, 500
    response = {'success': True}, 200
    return response

# --------- ITEMS ---------

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

# Users

def login(username, password):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
    cipher = hashlib.sha256()
    cipher.update(str(password).encode())
    pash = cipher.hexdigest()[:16]
    try:
        users = db.getUser(username)
    except Exception as e:
        print(str(e))
        return {
            'error': 'Delete Items Error', 
            'message':'Error deleting items: ' + str(e)}, 500

    if len(users) == 0:
        return {'error': 'Invalid Username', 'message': 'Cannot find user ' + str(username)}, 401
    if users[0][0] != username or users[0][1] != pash:
        return {'error': 'Invalid Credentials', 'message': 'Incorrect Password for user ' + str(username)}, 401

    token = jwt.encode({'Username': username, 'PasswordHash': pash}, SECRET_KEY, algorithm='HS256'),
    return {'token': token}, 200