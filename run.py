from flask import jsonify, make_response
import os

from app import creat_app
config_name = os.getenv("FLASK_ENV")
"""Gets the app settings defined in the .env file"""
app = creat_app(config_name)
"""defining the configuration to be used"""


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"message": "Page not found, Please check your URL"}), 404)


@app.errorhandler(405)
def url_not_found(error):
    return make_response(jsonify({'message': 'Requested method not allowed'}), 405)


@app.errorhandler(500)
def internal_server_error(e):
    return make_response(jsonify({"message": "Internal server error"}), 500)


@app.errorhandler(400)
def bad_request(e):
    return make_response(jsonify({"message": "Bad request"}), 400)


if __name__ == "__main__":
    app.run()
