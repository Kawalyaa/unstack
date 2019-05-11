import os
from flask import request, make_response, jsonify, Blueprint
# from flasgger import swag_from
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
            "access_token": str(token),
            "user_id": user_id
        }), 201)

    return make_response(jsonify({
        "message": "User exists"}), 409)
