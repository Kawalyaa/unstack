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

        self.log2 = {
            "user_name": "kuiawalya9aik",
            "password": "bornaga"
        }

        self.user2 = {
            "name": "Kawalyas",
            "user_name": "kawaandy",
            "password": "bornagaini",
            "email": "kawalyas@gmail.com"
        }
        self.question = {
            "title": "Tech News",
            "description": "Who is the founder of Tesla"
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

    def post2(self, path, auth):
        """This endpoint allows posting data for both authentication and open"""
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.post(path=path, headers=headers, content_type='application/json')
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

    # def post_question(self):
    #    """The user first login to post aquestion"""
    #    resp = self.normal_login()
    #    data = json.loads(resp.data.decode())
    #    token = data['access_token']
    #    res = self.post(path="api/v2/question", data=self.question, auth=token)
    #    return res

    def normal_login(self):
        self.post_user(path='api/v2/auth/signup')
        login = self.post(path='api/v2/auth/login', data=self.log, auth=None)
        return login

    def abnormal_login(self):
        self.post_user(path='api/v2/auth/signup')
        login = self.post(path='api/v2/auth/login', data=self.log2, auth=None)
        return login

    def logout(self):
        res = self.normal_login()
        # result = json.loads(login.data)
        data = json.loads(res.data.decode())
        token = data['access_token']
        logout = self.post2(path='api/v2/auth/logout', auth=token)
        return logout

    def post_questions(self):
        token = self.normal_login().json['access_token']
        res = self.post(path='api/v2/question', data=self.question, auth=token)
        return res

    def invalid_question(self):
        """Posting question with no token"""
        res = self.post(path='api/v2/question', data=self.question, auth=None)
        return res

    def tearDown(self):
        """This function destroys objests created during the test run"""

        with self.app.app_context():
            DataBaseConnection().drop_all_tables()
            self.db.close()
