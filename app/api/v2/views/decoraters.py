from functools import wraps
from app.api.v2.models.auth_models import UserModel
# from app.db_con import DataBaseConnection
from flask import request, jsonify, g, make_response


def auth_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        """Checks the validity of the header and raises a corresponding error"""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
                auth_token = ''
        if auth_token:
            resp = UserModel().decode_token(auth_token)
            if not isinstance(resp, str):
                try:
                    g.user = resp
                    return func(*args, **kwargs)
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403
    return wrap
