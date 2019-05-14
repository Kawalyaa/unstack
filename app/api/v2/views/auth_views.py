import os
from flask import request, make_response, jsonify, Blueprint
from flasgger import swag_from
from app.api.v2.models.auth_models import UserModel
from werkzeug.exceptions import BadRequest
import string
import re

auth = Blueprint('api_v2', __name__)

KEY = os.getenv("SECRET")


def validate_user(user):
    """This function validates the user input and rejects or accepts it"""
    for key, value in user.items():
        # ensure keys have values
        if not value:
            raise BadRequest("{} is lacking. It is required field".format(key))
        # validate length
        if key == "user_name" or key == "password":
            if len(value) < 4:
                raise BadRequest("The {} provided is too short, it should be 5 characters above".format(key))
            elif len(value) > 15:
                raise BadRequest("The {} provided is too long, it should be less than 15 characters".format(key))

        if key == "name":
            # make sure the value provided is a string
            for i in value:

                if i not in string.ascii_letters:
                    raise BadRequest("{} can not have non alphatic characters".format(key))
        if key == "email":
            # make sure email contains expetected characters
            if not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', value):
                raise BadRequest("The email provided is invalid")


@auth.route('/api/v2/auth/signup', methods=['POST'])
@swag_from('../docs/signup.yml')
def signup_user():
    req = request.get_json()

    if not req:
        return jsonify({"mesage": "Content should be json"})
    try:
        name = req['name'].strip()
        email = req['email'].strip()
        password = req['password'].strip()
        user_name = req['user_name'].strip()
    except ValueError:
        return jsonify({"message": "Incorect input"})
    new = {
        "name": name,
        "email": email,
        "password": password,
        "user_name": user_name
    }
    validate_user(new)
    requester = UserModel(**new)
    res = requester.save_user()
    # save user and return id
    if isinstance(res, int):
        user_id = res
        token = UserModel.ecnode_token(user_id)
        return make_response(jsonify({
            "message": "created successfully",
            "access_token": token.decode(),
            "user_id": user_id
        }), 201)

    return make_response(jsonify({
        "message": "User exists"}), 409)


@auth.route('/api/v2/auth/login', methods=['POST'])
@swag_from('../docs/login.yml')
def login_user():
    req = request.get_json()
    if not req:
        return jsonify({"message": "Content should be json"})
    user_name = req['user_name']
    password = req['password']

    login = {
        "user_name": user_name,
        "password": password
    }
    validate_user(login)
    res = UserModel().check_exists('users', 'user_name', login['user_name'])
    if res is False:
        return make_response(jsonify({
            "message": "No user found"
        }), 404)
    record = UserModel().get_user_by_username(login['user_name'])
    user_id, password = record
    # our user name has got the password and the user_id
    if password != login['password']:
        return make_response(jsonify({
            "message": "user_name and password does not much"
        }), 400)
    user = UserModel()
    token = user.ecnode_token(user_id)
    return make_response(jsonify({
        "message": "Welcome {}".format(login['user_name']),
        "access_token": token.decode()
    }), 200)


@auth.route('/api/v2/auth/logout', methods=['POST'])
@swag_from('../docs/logout.yml')
def logout_user():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
            auth_token = ''
    if auth_token:
        resp = UserModel().decode_token(auth_token)
        if not isinstance(resp, str):
            UserModel().logout(auth_token)
            try:
                return make_response(jsonify({
                    "message": "Loged out successfully"
                }), 200)
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
