import json
from app.tests.base_test import BaseTest
from app.db_con import DataBaseConnection


class TestQuestion(BaseTest):
    def tearDown(self):
        """This function destroys objests created during the test run"""
        DataBaseConnection().drop_all_tables()

    def test_posting_answers(self):
        # a different user to answer a question
        self.post_questions()
        res = self.post_answers()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["message"], "answer created")

    def test_posting_answers_twice(self):
        self.post_questions()
        self.post_answers()
        res = self.post_answers()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 409)
        self.assertEqual(data["message"], "Answer exists")

    def test_make_answer_user_prefered(self):
        # The person who posted the question
        self.post_questions()
        self.post_answers()
        res = self.make_user_prefered_answer()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], "user_preferd Successfully set")

    def test_editing_answer(self):
        # The person who posted the answer
        self.post_questions()
        self.post_answers()
        res = self.edit_answer()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['description'], "Answer with id 1 is updated")

    def test_vote_answer(self):
        self.post_questions()
        self.post_answers()
        res = self.vote_answer()
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['description'], "Answer voted successfully")
