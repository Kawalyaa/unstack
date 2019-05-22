from datetime import datetime, timedelta
import jwt
import string
import re
from flask import current_app
from app.db_con import DataBaseConnection as db_con


class BaseModel(db_con):
    """class to stracture the user"""
    @staticmethod
    def ecnode_token(user_id):
        """Generating the auth token returning a string"""
        try:
            payload = {
                # Token expiry date
                "exp": datetime.utcnow() + timedelta(minutes=30),
                # The time token is generated
                "iat": datetime.utcnow(),
                # User to be idenfied
                "sub": int(user_id)
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm="HS256"
            )  # .decode('utf-8')
        except Exception as e:
            return e

    def check_exists(self, table_name, field_name, value):
        con = self.init_db()
        cur = con.cursor()
        query = "SELECT * FROM {} WHERE {}='{}'".format(table_name, field_name, value)
        cur.execute(query)
        resp = cur.fetchone()
        con.commit()
        return resp is not None

    def blacklisted(self, token):
        con = self.init_db()
        cur = con.cursor()
        query = """
                SELECT * FROM blacklist WHERE tokens = %s;
                """
        cur.execute(query, [token])
        if cur.fetchone():
            return True
        return False

    def decode_token(self, auth_token):
        """This function takes in an authtoken and decodes it, returning an integer or string"""
        # secret = os.getenv("SECRET")
        # secret = current_app.config.get('SECRET')
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET'))
            if self.blacklisted(auth_token):
                return "Token has been blacklisted"
            # We decode the auth_token using the same secret key used to encode it
            # If it is valid we get or the user_id from the "user" index of payload
            else:
                return payload['sub']  # user_id
        except jwt.ExpiredSignatureError:
            return "The token has expired.Please log in again."
        except jwt.InvalidTokenError:
            return "The token is invalid.Please log in again."

    def delete_tb_value(self, table_name, field_name, value):
        if self.check_exists(table_name, field_name, value) is False:
            return "Item not found"
        con = self.init_db()
        cur = con.cursor()
        query = "DELETE FROM {} WHERE {}={};".format(table_name, field_name, value)
        cur.execute(query)
        con.commit()
        # self.save_incoming_data_or_updates(query)
        return "Deleted"

    def get_item_id(self, item_id, table_name, field_name, value):
        """This method takes id and returns id if found"""
        con = self.init_db()
        cur = con.cursor()
        query = "SELECT {} FROM {} WHERE {} = '{}'".format(item_id, table_name, field_name, value)
        cur.execute(query)
        id = cur.fetchone()[0]
        con.commit()
        return id

    def valid_string(self, data):
        if len(data) == 0:
            return ("Field should not be empty string")
        if not data:
            return ("It is a required field")

    def get_item(self, table_name, field_name, value):
        con = self.init_db()
        cur = con.cursor()
        query = "SELECT * FROM {} WHERE {}='{}'".format(table_name, field_name, value)
        cur.execute(query)
        resp = cur.fetchone()
        con.commit()
        return resp

    def validate_user(self, auser):
        """This function validates the user input and rejects or accepts it"""
        for key, value in auser.items():
            # ensure keys have values
            if not value:
                return ("{} is lacking. It is required field".format(key))
            # validate length
            if key == "user_name" or key == "password":
                if len(value) < 4:
                    return ("The {} provided is too short, it should be 5 characters above".format(key))
                elif len(value) > 15:
                    return ("The {} provided is too long, it should be less than 15 characters".format(key))

            if key == "name":
                # make sure the value provided is a string
                for i in value:

                    if i not in string.ascii_letters:
                        return ("{} can not have non alphatic characters".format(key))
            if key == "email":
                # make sure email contains expetected characters
                if not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', value):
                    return ("The email provided is invalid")
