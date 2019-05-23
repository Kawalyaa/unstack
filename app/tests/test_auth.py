import json
from app.tests.base_test import BaseTest
from app.db_con import DataBaseConnection


class TestAuth(BaseTest):
    def tearDown(self):
        """This function destroys objests created during the test run"""
        DataBaseConnection().drop_all_tables()
        self.db.close()

    def test_user_signup(self):
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
        self.assertEqual(res.status_code, 400)

    def test_user_logout(self):
        self.post_user(path='api/v2/auth/signup')
        res = self.post(path='api/v2/auth/login', data=self.log, auth=None)
        data = json.loads(res.data.decode())
        token = data['access_token']
        logout = self.post2(path='api/v2/auth/logout', auth=token)
        data2 = json.loads(logout.data.decode())
        self.assertEqual(data2['message'], "Loged out successfully")
        self.assertEqual(logout.status_code, 200)

    def test_another_logout(self):
        res = self.logout()
        data2 = json.loads(res.data.decode())
        self.assertEqual(data2['message'], "Loged out successfully")
        self.assertEqual(res.status_code, 200)
