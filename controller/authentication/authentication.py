from functools import wraps
import jwt
from flask import request, jsonify
from flask import current_app
from model.dbhandling import *
from model.connection_string import secret

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if token == 'undefined' or not token:
            return {
                'message': 'Authentication Token is missing!',
                'data': None,
                'error': 'Unauthorized'
            }, 401
        try:
            try:
                data = jwt.decode(token, secret, algorithms=['HS256'])
            except Exception as e:
                return {
                    'message': 'Invalid Authentication token!',
                    'data': None,
                    'error': 'Unauthorized'
                }, 403
            username = data['Username']
            password = data['PasswordHash']
            users = getUser(username)
            if len(users) < 0:
                return jsonify({'Error': 'Cannot find user ' + str(username)}), 400
            if users[0][0] != username or users[0][1] != password:
                return {
                    'message': 'Invalid Authentication token!',
                    'data': None,
                    'error': 'Unauthorized'
                }, 403
        except Exception as e:
            print(str(e))
            return {
                'message': 'Something went wrong',
                'data': None,
                'error': str(e)
            }, 500
        return f(*args, **kwargs)
    return decorated