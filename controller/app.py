from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_json_schema import JsonSchema, JsonValidationError
import os
from model.schemas import *
from controller.functions.get_functions import *
from controller.functions.post_functions import *
from functools import wraps
from controller.authentication.authentication import token_required

app = Flask(__name__)
schema = JsonSchema(app)
CORS(app)

# Ensures all endpoints will return successfully, even if an error occurs
def protection_wrapper(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(str(e))
            return jsonify({'error': str(e), 'message': str(e)}), 500
    return decorated
    

# --------- GET ENDPOINTS ---------

# Endpoint for getting a specified item by barcode
@app.route('/get_item', methods=['GET'])
@protection_wrapper
def get_item():
    barcode = str(request.args.get('barcode', default=''))
    return getItem(barcode)
    
# Endpoint for returning All Items seen by the db
@app.route('/get_items', methods=['GET'])
@protection_wrapper
def get_items():
    return getItems()

# Endpoint for getting all items in a project
@app.route('/get_project_items', methods=['GET'])
@protection_wrapper
def get_project_items():
    projectNumber = str(request.args.get('projectNumber', default=''))
    return getProjectItems(projectNumber)

# Endpoint for getting specified project
@app.route('/get_project', methods=['GET'])
@protection_wrapper
def get_project():
    projectNumber = str(request.args.get('projectNumber', default=''))
    return getProject(projectNumber)
    
# Endpoint for getting projects
@app.route('/get_projects', methods=['GET'])
@protection_wrapper
def get_projects():
    return getProjects()
    
# --------- POST ENDPOINTS ---------

@app.route('/add_project_items', methods=['POST'])
@schema.validate(project_items_schema)
@protection_wrapper
def add_project_items():
    data = request.json
    items = data['Entries']
    projectNumber = str(request.args.get('projectNumber', default=''))
    return addProjectItems(items, projectNumber)

@app.route('/add_project', methods=['POST'])
@schema.validate(project_schema)
@protection_wrapper
def add_project():
    data = request.json
    projectNumber = data['Project Number']
    projectName = data['Project Name']
    return addProject(projectNumber, projectName)

@app.route('/increment_project_items', methods=['POST'])
@schema.validate(project_items_schema)
@protection_wrapper
def increment_project_items():
    data = request.json
    projectNumber = str(request.args.get('projectNumber', default=''))
    items = data['Entries']
    return incrementProjectItems(items, projectNumber)

@app.route('/modify_project_items', methods=['POST'])
@schema.validate(project_items_schema)
@protection_wrapper
def modify_project_items():
    data = request.json
    projectNumber = str(request.args.get('projectNumber', default=''))
    items = data['Entries']
    return modifyProjectItems(items, projectNumber)

@app.route('/delete_project_items', methods=['POST'])
@schema.validate(project_items_schema)
@protection_wrapper
def delete_project_items():
    data = request.json
    projectNumber = str(request.args.get('projectNumber', default=''))
    items = data['Entries']
    return deleteProjectItems(items, projectNumber)

@app.route('/modify_all_items', methods=['POST'])
@schema.validate(items_schema)
@protection_wrapper
def modify_all_items():
    data = request.json
    items = data['Entries']
    return modifyItems(items)

@app.route('/delete_all_items', methods=['POST'])
@schema.validate(items_schema)
@protection_wrapper
def delete_all_items():
    data = request.json
    items = data['Entries']
    return deleteItems(items)

@app.route('/modify_projects', methods=['POST'])
@schema.validate(projects_schema)
@protection_wrapper
def modify_projects():
    data = request.json
    items = data['Entries']
    return modifyProjects(items)

@app.route('/delete_projects', methods=['POST'])
@schema.validate(projects_schema)
@protection_wrapper
def delete_projects():
    data = request.json
    items = data['Entries']
    return deleteProjects(items)

@app.route('/pull_from_stock', methods=['POST'])
@schema.validate(items_schema)
@protection_wrapper
def pull_from_stock():
    data = request.json
    items = data['Entries']
    projectNumber = str(request.args.get('projectNumber', default=''))
    return pullFromStock(items, projectNumber)

@app.route('/login', methods=['POST'])
@schema.validate(login_schema)
@protection_wrapper
def login_EP():
    data = request.json
    username = data['Username']
    password = data['Password']
    return login(username, password)

@app.route('/upload_BOM', methods=['POST'])
@schema.validate(project_items_schema)
@protection_wrapper
def upload_BOM():
    data = request.json
    projectNumber = str(request.args.get('projectNumber', default=''))
    items = data['Entries']
    return uploadBOM(items, projectNumber)

@app.route('/get_archived_projects', methods=['GET'])
@protection_wrapper
def get_archived_projects():
    return getArchivedProjects()

@app.route('/download_archived_csv/<path:filename>', methods=['GET'])
@schema.validate(project_schema)
@protection_wrapper
def get_archived_csv(filename):
    Path("../archives").mkdir(parents=True, exist_ok=True)
    full_path = os.path.join(app.root_path, '..\\..\\archives')
    return send_from_directory(full_path, filename)

@app.route('/reupload_BOM', methods=['POST'])
@schema.validate(project_items_schema)
@protection_wrapper
@token_required
def reupload_BOM():
    data = request.json
    projectNumber = str(request.args.get('projectNumber', default=''))
    items = data['Entries']
    return reuploadBOM(items, projectNumber)

@app.route('/upload_catalog', methods=['POST'])
@schema.validate(items_schema)
@protection_wrapper
@token_required
def upload_catalog():
    data = request.json
    items = data['Entries']
    return uploadCatalog(items)

# --------- ERROR HANDLING ---------

@app.errorhandler(JsonValidationError)
def validation_error(e):
    print(e)
    return {'error': str(e), 'message': [validation_error.message for validation_error  in e.errors]}, 500