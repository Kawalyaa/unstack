from flasgger import swag_from
from flask import request, make_response, jsonify, Blueprint, g
from app.api.v2.models.question_models import QuestionModel
from app.api.v2.views.decoraters import auth_required
from app.api.v2.models.answer_model import AnswersModel
from app.api.v2.models.auth_models import UserModel


question = Blueprint('question', __name__)


@question.route('/api/v2/question', methods=['POST'])
@swag_from('../docs/post_qtn.yml')
@auth_required
def post_question():
    """creating a blog and protecting routes"""
    user_id = g.user
    req = request.get_json()
    data = {
        "title": req["title"],
        "description": req["description"],
        "user_id": int(user_id)
    }
    QuestionModel().validate(data)
    requester = QuestionModel(**data)
    check = requester.get_item('questions', 'description', data["description"])
    if check:
        return jsonify({"message": "question already exists"}), 409
    question_id = requester.save()
    if isinstance(question_id, int):
        return make_response(jsonify({
            "message": "Question Created successfully",
            "question_id": question_id,
            "user_id": user_id
        }), 201)


@question.route('/api/v2/question', methods=['GET'])
@swag_from('../docs/get_all_qtn.yml')
@auth_required
def get_all_questions():
    """getting all questions"""
    res = QuestionModel().get_question()
    if res:
        return make_response(jsonify({
            "message": "ok",
            "questions": res
        }), 200)

    else:
        return make_response(jsonify({"message": "Database is empty"}))


@question.route('/api/v2/question/<int:question_id>', methods=['GET'])
@swag_from('../docs/get_one_qtn.yml')
@auth_required
def get_one_question(question_id):
    """get aquestion by id """

    result = QuestionModel().get_one_question(question_id)
    if result == "Not found":
        return make_response(jsonify({"message": "Question not found in the database"}), 404)

    else:
        return make_response(jsonify({
            "message": "ok",
            "question": result
        }), 200)


@question.route('/api/v2/question/<int:question_id>', methods=['PUT'])
@swag_from('../docs/edit_qtn.yml')
@auth_required
def edit_question(question_id):
    """Endpoint for editing a question"""
    if not request.json:
        return jsonify({"message": "Data should be in json format"})
    data = request.get_json()
    title = data['title']
    description = data['description']
    if QuestionModel().check_exists('questions', 'question_id', question_id) is False:
        return make_response(jsonify({"message": "Item  is not found in the database"}), 404)
    QuestionModel().update_question(title, description, question_id)

    return make_response(jsonify({
        "message": "question with id {} is updated".format(question_id)
    }), 200)


@question.route('/api/v2/question/<int:question_id>', methods=['DELETE'])
@swag_from('../docs/delete_qtn.yml')
@auth_required
def delete(question_id):
    """endpoint for deleting aquestion"""
    if QuestionModel().check_exists('questions', 'question_id', question_id) is False:
        return make_response(jsonify({"message": "No item found"}), 404)
    deleted = QuestionModel()
    # delete question
    deleted.delete_tb_value("questions", "question_id", question_id)
    message = "question with id {} is Deleted".format(question_id)
    return make_response(jsonify({"message": message}), 200)


@question.route('/api/v2/question/plus/answers/<int:question_id>', methods=['GET'])
@swag_from('../docs/get_qtn_and_ans.yml')
@auth_required
def get_qtn_and_ans(question_id):
    """Returns a question and all it's answers"""
    # get all question details
    question_details = QuestionModel().get_item("questions", "question_id", question_id)
    if not question_details:
        return jsonify({"message": "Not posts found"}), 404
    answers = AnswersModel().get_answers_by_question_id(int(question_id))
    question_id, title, description, user_id, created_on = question_details  # result from question_details
    user = UserModel().get_user_name_by_id(int(user_id))  # get user_name
    return make_response(jsonify({
        "message": "Success",
        "user_name": user,
        "title": title,
        "description": description,
        "user_id": int(user_id),
        "created_on": created_on,
        "answers": answers
    }), 200)


@question.route('/api/v2/question/most_answered', methods=['GET'])
@swag_from('../docs/get_most_answered_qtn.yml')
@auth_required
def get_most_answered():
    """This endpoint allows a user to get all the details to the question with the most answers"""
    question = QuestionModel()
    most_answered = question.most_answered()
    question_id, number = most_answered
    # get answer details using question_id
    answers = AnswersModel().get_answers_by_question_id(int(question_id))
    # get the post details using question_id
    most_answered_question = QuestionModel().get_item("questions", "question_id", int(question_id))
    question_id, title, description, user_id, created_on = most_answered_question
    user = UserModel().get_user_name_by_id(int(user_id))  # get user_name
    return make_response(jsonify({
        "message": "Success",
        "user_name": user,
        "question_id": question_id,
        "number": number,
        "title": title,
        "description": description,
        "created_on": created_on,
        "answers": answers
    }), 200)


@question.route('/api/v2/question/<user_name>', methods=['GET'])
@swag_from('../docs/get_user_qtn_by_name.yml')
@auth_required
def get_user_qtn(user_name):
    """returns all the questions associated with a particular user"""
    user_info = UserModel().get_user_by_username(user_name)
    if not user_info:
        return jsonify({"message": "The user_name does not exist"}), 404

    user_id, password = user_info  # for user_id, password in user_ifo
    ques = QuestionModel()
    question = ques.get_item("questions", "user_id", int(user_id))
    question_list = []
    if not question:
        return jsonify({"message": "Question not found"}), 404

    question_id, title, description, user_id, created_on = question
    quest_detail = {
        "question_id": int(question_id),
        "title": title,
        "description": description,
        "user_id": int(user_id),
        "created_on": created_on
    }
    question_list.append(quest_detail)
    return make_response(jsonify({
        "message": "ok",
        "user": user_name,
        "question": question_list
    }), 200)


@question.route('/api/v2/question/answer/<int:question_id>', methods=['DELETE'])
@swag_from('../docs/delete_qtn_and_ans.yml')
@auth_required
def delete_qtn_and_ans(question_id):
    """Endpoint for deleting aquestion and its answers"""
    check = QuestionModel().check_exists("questions", "question_id", question_id)
    if check is False:
        return jsonify({"message": "question not found"}), 404
    delete = QuestionModel().delete_question_and_its_answers(question_id)
    return make_response(jsonify({"message": delete}), 200)


@question.route('/api/v2/question/noauth', methods=['GET'])
@swag_from('../docs/get_all_qtn.yml')
def get_all():
    """getting all questions"""
    res = QuestionModel().get_question()
    if res:
        return make_response(jsonify({
            "message": "ok",
            "questions": res
        }), 200)

    else:
        return make_response(jsonify({"message": "Database is empty"}))
