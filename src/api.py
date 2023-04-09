import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

URL_AUTH = os.getenv('AUTH0_DOMAIN', 'taint24.us.auth0.com')
AUDIENCE = os.getenv('API_AUDIENCE', 'fsnd')
CLIENT_ID = os.getenv('CLIENT_ID', '')
CALLBACK_URL = os.getenv('CALLBACK_URL', '')

# ROUTES
@app.route('/')
def welcome():
    try:
        link = 'https://'
        link += URL_AUTH
        link += '/authorize?'
        link += 'audience=' + AUDIENCE + '&'
        link += 'response_type=token&'
        link += 'client_id=' + CLIENT_ID + '&'
        link += 'redirect_uri=' + CALLBACK_URL + '/'
        return link

    except Exception:
        abort(422)


# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(error):
    print(error)
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code