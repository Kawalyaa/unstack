import json
from app.tests.base_test import BaseTest
from app.db_con import DataBaseConnection


class TestAuth(BaseTest):

    def test_user_signup(self):
        DataBaseConnection().drop_all_tables()
        reg = self.post_user(path='api/v2/auth/signup')
        data = json.loads(reg.data.decode())
        self.assertEqual(data['message'], "created successfully")
        self.assertEqual(reg.status_code, 201)
        self.assertTrue(data['access_token'])

    def test_registered_user(self):
        reg = self.post_user(path='api/v2/auth/signup')
        data = json.loads(reg.data.decode())
        self.assertEqual(data['message'], "User exists")
        self.assertEqual(reg.status_code, 409)
