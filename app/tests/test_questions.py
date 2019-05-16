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

    def test_getting_questions(self):
        self.post_questions()
        res = self.get_questions()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], "ok")

    def test_getting_questions_from_empty_database(self):
        res = self.get_questions()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], "Database is empty")

    def test_getting_one_question(self):
        self.post_questions()
        res = self.get_one_question()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], "ok")

    def test_getting_missing_question(self):
        res = self.get_one_question()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "Question not found in the database")

    def test_editing_question(self):
        self.post_questions()
        res = self.edit_question()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], "question with id 1 is updated")

    def test_editing_question_not_existing(self):
        res = self.edit_question()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "Item  is not found in the database")
        self.assertTrue(data['message'])

    def test_deleting_question(self):
        self.post_questions()
        res = self.delete_question()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], "question with id 1 is Deleted")
        self.assertTrue(data['message'])

    def test_deleting_un_existing_question(self):
        res = self.delete_question()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "No item found")
        self.assertTrue(data['message'])

    def test_get_question_and_its_answers(self):
        self.post_questions()
        self.post_answers()
        res = self.get_qtn_and_ans()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], "Success")

    def test_most_answered_question(self):
        self.post_questions()
        self.post_answers()
        res = self.get_most_answered()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], "Success")

    def test_get_question_by_user_name(self):
        self.post_questions()
        res = self.get_qtn_by_name()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], "ok")

    def test_delete_question_and_its_answers(self):
        self.post_questions()
        self.post_answers()
        res = self.delete_ques_and_ans()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], "question with id 1 and its answers deleted")

    def test_welcomee(self):
        res = self.welcome()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], "WELCOME TO UNSTACK APP")
