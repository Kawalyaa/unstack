import unittest
from app.db_con import DataBaseConnection
from app import creat_app
import json


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.app = creat_app('testing')
        self.client = self.app.test_client()

        self.user = {
            "name": "Kawalya",
            "user_name": "kuiawalya9aik",
            "password": "bornagain",
            "email": "kawaly@gmail.com"
        }

        self.log = {
            "user_name": "kuiawalya9aik",
            "password": "bornagain"
        }

        self.user2 = {
            "name": "Kawalyas",
            "user_name": "kawaandy",
            "password": "bornagaini",
            "email": "kawalyas@gmail.com"
        }

        with self.app.app_context():
            self.db = DataBaseConnection().init_db()

    def get_headers(self, authtoken=None):
        headers = {
            "Authorization": 'Bearer {}'.format(authtoken),
            "content_type": 'application/json'
        }
        return headers

    def post(self, path, data, auth):
        """This endpoint allows posting data for both authentication and open"""
        dto = json.dumps(data)
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.post(path=path, data=dto, headers=headers, content_type='application/json')
        return res

    def get(self, path, auth):
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.get(path=path, headers=headers, content_type='application/json')
        return res

    def post_user(self, path=""):
        if not path:
            path = 'api/v2/auth/signup'
        res = self.post(path=path, data=self.user, auth=None)
        return res

    def post_question(self):
        res = self.post(path="/question", data=self.qustion, auth=None)
        return res

    def normal_login(self):
        self.post_user(path='/auth/signup')
        login = self.post(path='/auth/login', data=self.log, auth=None)
        return login

    def login(self):
        self.post_user(path='/auth/signup')
        payload = {
            "user_name": self.user['user_name'],
            "password": self.user['password']
        }
        login = self.post(path='/auth/login', data=payload, auth=None)
        result = json.loads(login.data)
        token = result['access_token']
        return token

    def post_questions(self):
        question = {
            "title": "WORLDI NEWZ",
            "description": "Where are the tesla factories found"
        }
        token = self.normal_login().json['access_token']
        res = self.post(path='/question', data=question, auth=token)
        return res
