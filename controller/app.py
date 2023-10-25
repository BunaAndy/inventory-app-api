from flask import Flask, jsonify
from flask import request
from flask_cors import CORS
from flask_json_schema import JsonSchema, JsonValidationError
import model.dbhandling as db
import os
import jwt
import hashlib
from model.schemas.item_schema import item_schema
from model.schemas.items_schema import items_schema
from model.schemas.project_schema import project_schema
from model.schemas.projects_schema import projects_schema

app = Flask(__name__)
schema = JsonSchema(app)
CORS(app)

SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
app.config['SECRET_KEY'] = SECRET_KEY

# Endpoint for getting 
@app.route('/get_projects', methods=['GET'])
def get_projects():
    try:
        try:
            projects = db.getAllProjects()
        except Exception as e:
            print(e)
            return jsonify({
                'error': 'Get Projects Error',
                'message':'Error fetching all Projects: ' + str(e)}), 500  

        try:
            projectCols = db.getColumns('Projects')
        except Exception as e:
            print(e)
            return jsonify({
                'error': 'Get Columns Error',
                'message':'Error fetching columns of Project_Items' + ': ' + str(e)}), 500

        response = jsonify({
            'entries': projects, 
            'projectNumber': 'All Projects', 
            'name': 'All Projects', 
            'columns': projectCols, 
            'success': True})
        return response, 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e), 'message': str(e)}), 500

# Endpoint fro returning All Items seen by the db
@app.route('/get_items', methods=['GET'])
def get_items():
    try:
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
                'message':'Error fetching columns of All Items: ' + str(e)}), 500

        # Creates json with output data
        response = jsonify({
            'entries': items,
            'projectNumber': 'All Items',
            'name': 'All Items',
            'columns': allItemsCols,
            'success': True})
        return response, 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e), 'message': str(e)}), 500

# Endpoint for getting all items in a project
@app.route('/get_project_items', methods=['GET'])
def get_project_items():
    try:
        projectNumber = str(request.args.get('project'))
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
                'message':'Error fetching columns of  ' + str('Project_Items') + ': ' + str(e)}), 500

        projectName = project['Project Name']

        # Creates json with output data
        response = jsonify({
            'entries': projectData,
            'projectNumber': projectNumber,
            'name': projectName,
            'columns': projectCols,
            'success': True})
        return response, 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e), 'message': str(e)}), 500
    
