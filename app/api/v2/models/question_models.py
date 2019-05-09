from werkzeug.exceptions import BadRequest
from app.api.v2.models.base_model import BaseModel
from datetime import datetime


class QuestionModel(BaseModel):
    """class for question models inheriting from BaseModel"""
    def __init__(self, title='title', description='description', user_id=0):
        self.title = title
        self.description = description
        self.user_id = user_id
        self.created_on = datetime.now()

    def validate(self, the_input):
        for key, value in the_input.items():
            if not value:
                raise BadRequest("{} should not be empty".format(key))
            if key == "title" or key == "description":
                if isinstance(value, int):
                    raise BadRequest("{} value should be a string".format(key))

    def save(self):
        """This method saves the post infomation"""
        question = {
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id
        }
        # if self.check_exists('questions', 'description', question['description']) is True:
        #    return jsonify({"message": "question exists"}), 409
        con = self.init_db()
        cur = con.cursor()
        query = """INSERT INTO questions (title, description, user_id, created_on) VALUES \
         (%(title)s, %(description)s, %(user_id)s, ('now')) RETURNING question_id;"""
        cur.execute(query, question)
        question_id = cur.fetchone()[0]
        con.commit()
        return int(question_id)

    def get_question(self):
        con = self.init_db()
        cur = con.cursor()
        query = "SELECT * FROM questions;"
        cur.execute(query)
        data = cur.fetchall()
        res = []

        for i, items in enumerate(data):
            question_id, title, description, user_id, created_on = items
            question = dict(
                question_id=question_id,
                title=title,
                description=description,
                user_id=int(user_id),
                created_on=str(created_on)
            )
            res.append(question)
        return res

    def get_one_question(self, question_id):
        """Method to get a single question"""

        if self.check_exists('questions', 'question_id', question_id) is False:
            return ("Not found")
        con = self.init_db()
        cur = con.cursor()
        query = "SELECT title, description, user_id, created_on FROM questions WHERE question_id={};".format(question_id)
        cur.execute(query)
        data = cur.fetchone()
        res = []

        question = dict(
            title=data[0],
            description=data[1],
            user_id=int(data[2]),
            created_on=str(data[3])
        )
        res.append(question)
        return res
