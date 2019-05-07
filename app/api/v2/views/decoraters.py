from functools import wraps
from app.api.v2.models.auth_models import UserModel
from app.db_con import DataBaseConnection
from flask import request, jsonify


def login_required(func):
    """
    login_required. protects a route to only authenticated users
    """
    @wraps(func)
    def auth(*args, **kwargs):

        access_token = request.headers.get('token', '')
        if not access_token:
            return jsonify({"message": "This route is protected, provide token"}), 401
        try:
            con = DataBaseConnection.init_db()
            cur = con.cursor()
            response = UserModel().decode_token(access_token)
            cur.execute("SELECT * FROM users WHERE user_id = '%s'" % response)
            get_user = cur.fetchone()
            user_info = list(get_user)
            user = UserModel(*user_info)
            return func(user, *args, **kwargs)
        except ValueError:
            return jsonify({'message': response}), 401

    return auth
