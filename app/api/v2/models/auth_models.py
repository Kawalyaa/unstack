# from functools import wraps
# from flask import request, g
# from werkzeug.exceptions import BadRequest, Unauthorized
from app.api.v2.models.base_model import BaseModel


class UserModel(BaseModel):
    """class for user models inheriting from BaseModel"""
    def __init__(self, name='name', email='email', password='password', user_name='user_name'):
        self.name = name
        self.email = email
        self.password = password
        self.user_name = user_name

    def save_user(self):
        """This method saves the user infomation"""
        user = {
            "name": self.name,
            "user_name": self.user_name,
            "email": self.email,
            "password": self.password
        }

        query = """INSERT INTO users (name, user_name, email, password) VALUES \
        (%(name)s, %(user_name)s, %(email)s, %(password)s) RETURNING user_id"""
        if self.check_exists('users', 'user_name', user['user_name']) is True:
            return("User already exists")
        con = self.init_db()
        cur = con.cursor()
        cur.execute(query, user)
        user_id = cur.fetchone()[0]
        con.commit()
        return int(user_id)

    def logout(self, token):
        """This method keeps used tokens in the blacklist table"""
        con = self.init_db()
        cur = con.cursor()
        inputs = {
            "tokens": token
        }
        query = """
                INSERT INTO blacklist
                VALUES (%(tokens)s) RETURNING tokens;
                """
        cur.execute(query, inputs)
        blacklisted_token = cur.fetchone()[0]
        con.commit()
        cur.close()
        return blacklisted_token
        # self.save_incoming_data_or_updates(query)

    def get_user_by_username(self, user_name):
        con = self.init_db()
        cur = con.cursor()
        query = """SELECT user_id, password \
        FROM users WHERE user_name = '{}'""".format(user_name)
        cur.execute(query)
        user_info = cur.fetchone()
        con.commit()
        # user_info = self.fetch_single_data_row(query)
        return user_info

    def get_user_name_by_id(self, user_id):
        con = self.init_db()
        cur = con.cursor()
        query = "SELECT user_name FROM users WHERE user_id = {};".format(int(user_id))
        cur.execute(query)
        user_name = cur.fetchone()
        con.commit()
        return user_name
