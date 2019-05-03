import json
from app.tests.base_test import BaseTest
from app.db_con import DataBaseConnection


class TestAuth(BaseTest):
    def tearDown(self):
        """This function destroys objests created during the test run"""
        DataBaseConnection().drop_all_tables()
        self.db.close()

    def test_user_signup(self):
        # DataBaseConnection().drop_all_tables()
        reg = self.post_user(path='api/v2/auth/signup')
        data = json.loads(reg.data.decode())
        self.assertEqual(data['message'], "created successfully")
        self.assertEqual(reg.status_code, 201)
        self.assertTrue(data['access_token'])

    def test_registered_user(self):
        self.post_user(path='api/v2/auth/signup')
        reg = self.post_user(path='api/v2/auth/signup')
        data = json.loads(reg.data.decode())
        self.assertEqual(data['message'], "User exists")
        self.assertEqual(reg.status_code, 409)

    def test_user_login(self):
        res = self.normal_login()
        data = json.loads(res.data.decode())
        self.assertEqual(data['message'], "Welcome kuiawalya9aik")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['access_token'])

    def test_unmuching_creds(self):
        res = self.abnormal_login()
        data = json.loads(res.data.decode())
        self.assertEqual(data['message'], "user_name and password does not much")
        self.assertEqual(res.status_code, 401)
