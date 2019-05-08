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
        if self.check_exists('questions', 'description', question['description']) is True:
            return ('question exists')
        con = self.init_db()
        cur = con.cursor()
        query = """INSERT INTO questions (title, description, user_id, created_on) VALUES \
         (%(title)s, %(description)s, %(user_id)s, ('now')) RETURNING question_id;"""
        cur.execute(query, question)
        question_id = cur.fetchone()[0]
        con.commit()
        return int(question_id)
