from datetime import datetime
from app.api.v2.models.auth_models import UserModel
from app.api.v2.models.base_model import BaseModel


class AnswersModel(BaseModel):
    def __init__(self, user_id="user_id", question_id="question_id", description="description"):
        self.user_id = user_id
        self.question_id = question_id
        self.description = description
        self.date_created = datetime.now()

    def save_answer(self):
        """Add answer details to the database"""
        answer = {
            "user_id": self.user_id,
            "question_id": self.question_id,
            "description": self.description,
            "date_created": self.date_created,
            "up_votes": 0
        }

        con = self.init_db()
        cur = con.cursor()
        query = """INSERT INTO answers (question_id, user_id, description, up_votes, date_created) VALUES \
        (%(question_id)s, %(user_id)s, %(description)s, %(up_votes)s, ('now')) RETURNING answer_id;"""
        cur.execute(query, answer)
        answer_id = cur.fetchone()[0]  # this means answer_id is returned in list and should be the first in list
        con.commit()
        cur.close()
        return int(answer_id)

    def toggle_user_prefered(self, answer_id):
        """This function marks answer as user prefered"""
        con = self.init_db()
        cur = con.cursor()
        query = "UPDATE answers SET user_preferred = NOT user_preferred WHERE answer_id={} RETURNING user_preferred;".format(int(answer_id))
        cur.execute(query)
        user_preferd = cur.fetchone()[0]
        con.commit()
        return user_preferd

    def vote_answer(self, answer_id, vote):
        """This method increments or decrement the up_votes field"""
        con = self.init_db()
        cur = con.cursor()
        query = "UPDATE answers SET up_votes = up_votes + {} WHERE answer_id={} RETURNING up_votes;".format(vote, answer_id)
        cur.execute(query)
        up_votes = cur.fetchone()[0]
        con.commit()
        return up_votes

    def get_answers_by_question_id(self, question_id):
        """return all answers of a given question"""
        con = self.init_db()
        cur = con.cursor()
        query = "SELECT * FROM answers WHERE question_id={};".format(int(question_id))
        cur.execute(query)
        data = cur.fetchall()
        res = []
        for i, items in enumerate(data):  # return items in order with index
            answer_id, question_id, user_id, description, up_votes, date_created, user_preferred = items
            user_name = UserModel().get_user_name_by_id(user_id)
            answer = {
                "answer_id": answer_id,
                "question_id": int(question_id),
                "user_id": int(user_id),
                "user_name": user_name,
                "description": description,
                "up_votes": int(up_votes),
                "date_created": date_created,
                "user_preferd": user_preferred
            }
            res.append(answer)
        return res

    def update_answer(self, description, answer_id):
        con = self.init_db()
        cur = con.cursor()
        query = "UPDATE answers SET description = '{}' WHERE answer_id = '{}'".format(description, answer_id)
        cur.execute(query)
        con.commit()
