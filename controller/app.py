from flask import Flask, jsonify
from flask import request
from flask_cors import CORS
from flask_json_schema import JsonSchema, JsonValidationError
import os
import jwt
import hashlib
from model.schemas.item_schema import item_schema
from model.schemas.items_schema import items_schema
from model.schemas.project_schema import project_schema
from model.schemas.projects_schema import projects_schema
from controller.functions.get_functions import *
from controller.functions.post_functions import *
from functools import wraps

app = Flask(__name__)
schema = JsonSchema(app)
CORS(app)

SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
app.config['SECRET_KEY'] = SECRET_KEY

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
@schema.validate(items_schema)
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

# --------- ERROR HANDLING ---------

@app.errorhandler(JsonValidationError)
def validation_error(e):
    print(e)
    return {'error': str(e), 'message': [validation_error.message for validation_error  in e.errors]}, 500