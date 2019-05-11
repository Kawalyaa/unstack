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

        self.second_user = {
            "name": "Kawalyaa",
            "user_name": "kawalya",
            "password": "bornagaini",
            "email": "kawaly@gmail.com"
        }

        self.second_log = {
            "user_name": "kawalya",
            "password": "bornagaini"
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
        self.question2 = {
            "title": "Tech News",
            "description": "Who is the founder of Tesla and spacex"
        }

        self.answers = {
            "title": "Tech News",
            "description": "He is called Elon Musk"
        }

        self.answers2 = {
            "title": "Tech News",
            "description": "He is called Elon Musk a 42yrs old"
        }
        self.vote = {
            "up_votes": 1
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
        """This method allows posting data for both authentication and open"""
        dto = json.dumps(data)
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.post(path=path, data=dto, headers=headers, content_type='application/json')
        return res

    def put(self, path, data, auth):
        """This method allows posting data for both authentication and open"""
        dto = json.dumps(data)
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.put(path=path, data=dto, headers=headers, content_type='application/json')
        return res

    def delete(self, path, auth):
        """This method allows deleting data for  authentication"""
        if auth is None:
            headers = None
        else:
            headers = self.get_headers(authtoken=auth)
        res = self.client.delete(path=path, headers=headers, content_type='application/json')
        return res

    def post2(self, path, auth):
        """This method allows posting without providing data eg logout"""
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
            path = '/api/v2/auth/signup'
        res = self.post(path=path, data=self.user, auth=None)
        return res

    def post_user2(self, path=""):
        # second_user signup
        if not path:
            path = '/api/v2/auth/signup'
        res = self.post(path=path, data=self.second_user, auth=None)
        return res

    def normal_login(self):
        self.post_user(path='/api/v2/auth/signup')
        login = self.post(path='/api/v2/auth/login', data=self.log, auth=None)
        return login

    def second_login(self):
        # second user login
        self.post_user2(path='/api/v2/auth/signup')
        login = self.post(path='/api/v2/auth/login', data=self.second_log, auth=None)
        return login

    def abnormal_login(self):
        self.post_user(path='/api/v2/auth/signup')
        login = self.post(path='/api/v2/auth/login', data=self.log2, auth=None)
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
        res = self.post(path='/api/v2/question', data=self.question, auth=token)
        return res

    def invalid_question(self):
        """Posting question with no token"""
        res = self.post(path='/api/v2/question', data=self.question, auth=None)
        return res

    def get_questions(self):
        token = self.normal_login().json['access_token']
        res = self.get(path='/api/v2/question', auth=token)
        return res

    def get_one_question(self):
        token = self.normal_login().json['access_token']
        res = self.get(path='/api/v2/question/1', auth=token)
        return res

    def edit_question(self):
        token = self.normal_login().json['access_token']
        res = self.put(path='/api/v2/question/1', data=self.question2, auth=token)
        return res

    def delete_question(self):
        token = self.normal_login().json['access_token']
        res = self.delete(path='/api/v2/question/1', auth=token)
        return res

    def post_answers(self):
        token = self.second_login().json['access_token']
        res = self.post(path='/api/v2/answers/1', data=self.answers, auth=token)
        return res

    def make_user_prefered_answer(self):
        token = self.normal_login().json['access_token']
        res = self.put('/api/v2/question/1/answers/1', data=self.answers2, auth=token)
        return res

    def edit_answer(self):
        token = self.second_login().json['access_token']
        res = self.put('/api/v2/question/1/answers/1', data=self.answers2, auth=token)
        return res

    def vote_answer(self):
        token = self.normal_login().json['access_token']
        res = self.put('/api/v2/question/1/answers/1/vote', data=self.vote, auth=token)
        return res

    def get_qtn_and_ans(self):
        token = self.normal_login().json['access_token']
        res = self.get(path='/api/v2/question/plus/answers/1', auth=token)
        return res

    def tearDown(self):
        """This function destroys objests created during the test run"""

        with self.app.app_context():
            DataBaseConnection().drop_all_tables()
            self.db.close()
