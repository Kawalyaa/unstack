from flask import request, jsonify, make_response, Blueprint, g
from werkzeug.exceptions import BadRequest
# from app.api.v2.models.question_models import QuestionModel
from app.api.v2.models.answer_model import AnswersModel
from app.api.v2.views.decoraters import auth_required
from app.api.v2.models.base_model import BaseModel


answer = Blueprint('answer', __name__)


def validate_input(data):
    for key, value in data.items():
        if not value:
            raise BadRequest("The{} is lacking. It is a required field".format(key))
        if key == "description":
            if len(value) < 10:
                raise BadRequest("The{} is too short. It should 10 characters and above".forrmat(key))


def check_exists_question_id_and_user_id(question_id, user_id):
    """Check if question_id and user_id passed in the url exists in the db"""
    question = AnswersModel().check_exists("questions", "question_id", question_id)
    user = AnswersModel().check_exists("users", "user_id", user_id)
    if question is False or user is False:
        return ("The question_id or user_id is not found")


def check_exists_question_id_and_answer_id(question_id, answer_id):
    """Check if question_id and answer_id passed in the url exists in the db"""
    question = AnswersModel().check_exists("questions", "question_id", question_id)
    user = AnswersModel().check_exists("answers", "answer_id", answer_id)
    if question is False or user is False:
        return ("The question_id or answer_id is not found")


@answer.route('/api/v2/answers/<int:question_id>', methods=['POST'])
@auth_required
def post_answer(question_id):
    """This endpoint handles posting answers to a question"""
    user_id = g.user  # geting the user from auth(decorators)
    req = request.get_json()
    answer = {
        "description": req['description'],
        "question_id": int(question_id),
        "user_id": user_id
    }
    validate_input(answer)
    ans_req = AnswersModel(**answer)
    check = check_exists_question_id_and_user_id(answer['question_id'], answer['user_id'])
    if check == "The question_id or user_id is not found":
        return jsonify({"message": "The question_id or user_id is not found"})

    if AnswersModel().check_exists("answers", "description", answer['description']) is True:
        return jsonify({"message": "Answer exists"}), 409
    answer_id = ans_req.save_answer()
    if isinstance(answer_id, int):
        return make_response(jsonify({
            "message": "answer created",
            "answer_id": answer_id,
            "user_id": user_id
        }), 201)


@answer.route('/api/v2/question/<int:question_id>/answers/<int:answer_id>', methods=['PUT'])
@auth_required
def edit_answer(question_id, answer_id):
    """
    This function is restricted to the author of the answer and the author of the question to edit or mark an answer as preferred.
    The ```answer_author_id``` is allowed to edit the answer.
    The ```question_author_id``` is allowed to mark the answer as preferred
    """
    check_id = check_exists_question_id_and_answer_id(question_id, answer_id)
    if check_id == "The question_id or answer_id is not found":
        return jsonify({"message": "question_id or answer_id provided is not found"})
    # Get the user_id of questions and answers using question_id and answer_is
    question_author_id = BaseModel().get_item_id('user_id', 'questions', 'question_id', question_id)
    answer_author_id = BaseModel().get_item_id('user_id', 'answers', 'answer_id', answer_id)

    if not question_author_id or not answer_author_id:
        return ("Question or answer details not found")

    user_id = g.user  # current user_id
    # search for answer owner
    if user_id == int(answer_author_id) and user_id != int(question_author_id):
        req = request.get_json()
        desc = req['description']
        AnswersModel().valid_string(desc)  # check for empty strings
        AnswersModel().update_answer(desc, answer_id)
        return make_response(jsonify({
            "message": "Success",
            "description": "Answer with id {} is updated".format(answer_id)
        }), 200)
    # search for question owner
    elif user_id == int(question_author_id) and user_id != int(answer_author_id):
        user_prefered = "{}".format(AnswersModel().toggle_user_prefered(answer_id))
        return make_response(jsonify({
            "message": "user_preferd Successfully set",
            "description": "answer updated successfully",
            "user_preferd": user_prefered
        }), 200)

    else:
        return make_response(jsonify({"message": "Your not authorised to edit this answer"}), 401)
