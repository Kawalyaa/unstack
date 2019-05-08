import json
from app.tests.base_test import BaseTest
from app.db_con import DataBaseConnection


class TestQuestion(BaseTest):
    def tearDown(self):
        """This function destroys objests created during the test run"""
        DataBaseConnection().drop_all_tables()
        self.db.close()

    def test_post_question(self):
        """Post question with token"""
        res = self.post_questions()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['message'], "Question Created successfully")
        self.assertTrue(data["message"])

    def test_post_with_no_token(self):
        """Posting question with no token"""
        res = self.invalid_question()
        self.assertEqual(res.status_code, 403)

    def test_posting_question_that_exists(self):
        self.post_questions()
        res = self.post_questions()
        self.assertEqual(res.status_code, 409)
