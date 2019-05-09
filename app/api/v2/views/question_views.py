# from flasgger import swag_from
from flask import request, make_response, jsonify, Blueprint
from app.api.v2.models.question_models import QuestionModel
from app.api.v2.views.decoraters import auth_required
# from app.api.version2.models.answers_model import AnswersModel
# from app.api.version2.models.user_model import UserModel
# from werkzeug.exceptions import NotFound

question = Blueprint('question', __name__)


@question.route('/api/v2/question', methods=['POST'])
def post_question():
    """creating a blog and protecting routes"""

    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
            auth_token = ''
    if auth_token:
        resp = QuestionModel().decode_token(auth_token)
        if not isinstance(resp, str):
            user_id = resp
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
            post_id = requester.save()
            if isinstance(post_id, int):
                try:
                    return make_response(jsonify({
                        "message": "Question Created successfully",
                        "post_id": post_id,
                        "user_id": user_id
                    }), 201)
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403


@question.route('/api/v2/question', methods=['GET'])
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


@question.route('/api/v2/question/<int:question_id>')
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
