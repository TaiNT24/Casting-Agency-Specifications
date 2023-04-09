import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from datetime import datetime

from database.models import db_drop_and_create_all, setup_db, Actors, Movies
from auth.auth import AuthError, requires_auth

URL_AUTH = os.getenv('AUTH0_DOMAIN', 'taint24.us.auth0.com')
AUDIENCE = os.getenv('API_AUDIENCE', 'fsnd')
CLIENT_ID = os.getenv('CLIENT_ID', 'MPl6C6iyk95MKm7MDG4MV1CNrghVjB8n')
CALLBACK_URL = os.getenv('CALLBACK_URL', 'http://localhost:5000')

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    db_drop_and_create_all()

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

    @app.route('/logout')
    def logout():
        try:
            link = 'https://'
            link += URL_AUTH
            link += '/v2/logout?'
            link += 'client_id=' + CLIENT_ID + '&'
            link += 'returnTo=' + CALLBACK_URL + '/logout'
            return link
        except Exception:
            abort(422)

    @app.route('/actors')
    @requires_auth('read:actors')
    def get_actors(payload):
        try:
            actors = Actors.query.all()
            actors_list = [actor.description() for actor in actors]

            return {
                "success": True,
                "actors": actors_list
            }
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies')
    @requires_auth('read:movies')
    def get_movies(payload):
        try:
            movies = Movies.query.all()
            movies_list = [movie.description() for movie in movies]

            return {
                "success": True,
                "movies": movies_list
            }
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors', methods=["POST"])
    @requires_auth('add:actors')
    def add_actors(payload):
        if type(request.json.get('name')) != str \
                or type(request.json.get('age')) != int:
            abort(422, {
                'message': 'name and age is required and string for name and int for age'
            })

        if type(request.json.get('gender')) != int \
                or request.json.get('gender') not in (0, 1):
            abort(422, {
                'message': 'gender is required and 0 for man and 1 for women'
            })

        try:
            actor = Actors()
            actor.name = request.json.get('name')
            actor.age = request.json.get('age')
            actor.gender = request.json.get('gender')
            actor.insert()

            return {
                "success": True,
                "actors": actor.description()
            }
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors/<actor_id>', methods=["DELETE"])
    @requires_auth('delete:actors')
    def delete_actors(payload, actor_id):
        actor = Actors.query.filter_by(id=actor_id).first()
        if not actor:
            abort(404)

        try:
            actor.delete()

            return {
                "success": True,
                "id": actor_id
            }
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors/<actor_id>', methods=["PATCH"])
    @requires_auth('update:actors')
    def update_actors(payload, actor_id):
        if 'name' in request.json and type(request.json.get('name')) != str:
            abort(422, {
                'message': 'data for name is string'
            })

        if 'age' in request.json and type(request.json.get('age')) != int:
            abort(422, {
                'message': 'data for name is integer'
            })

        if 'gender' in request.json\
                and request.json.get('gender') not in (0, 1):
            abort(422, {
                'message': 'data for gender is integer: 0 for man and 1 for women'
            })

        actor = Actors.query.filter_by(id=actor_id).first()
        if not actor:
            abort(404)

        try:
            name = request.json.get('name')
            if name:
                actor.name = name
            age = request.json.get('age')
            if age:
                actor.age = age
            gender = request.json.get('gender')
            if gender:
                actor.gender = gender

            actor.update()

            return {
                "success": True,
                "actor": actor.description()
            }
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies/<movie_id>', methods=["PATCH"])
    @requires_auth('update:movies')
    def update_movies(payload, movie_id):
        if 'release_date' in request.json and type(request.json.get('release_date')) != str:
            abort(422, {
                'message': 'data for release_date is string with format YYYY-mm-dd'
            })
        elif 'release_date' in request.json and type(request.json.get('release_date')) == str:
            try:
                datetime.strptime(request.json.get('release_date'), '%Y-%m-%d')
            except Exception as e:
                abort(422, {
                'message': 'data for release_date is string with format YYYY-mm-dd'
            })

        movie = Movies.query.filter_by(id=movie_id).first()
        if not movie:
            abort(404)

        try:
            release_date = request.json.get('release_date')
            if release_date:
                movie.release_date = datetime.strptime(release_date, '%Y-%m-%d')

            movie.update()

            return {
                "success": True,
                "movie": movie.description()
            }
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies', methods=["POST"])
    @requires_auth('add:movies')
    def add_movies(payload):
        if type(request.json.get('title')) != str:
            abort(422, {
                'message': 'title is required and data type is string'
            })

        try:
            release_date = datetime.strptime(request.json.get('release_date'), '%Y-%m-%d')
        except Exception as e:
            abort(422, {
                'message': 'release_date is required and data type is string with format YYYY-mm-dd'
            })

        try:
            movie = Movies()
            movie.title = request.json.get('title')
            movie.release_date = release_date
            movie.insert()

            return {
                "success": True,
                "movie": movie.description()
            }
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies/<movie_id>', methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movies(payload, movie_id):
        movie = Movies.query.filter_by(id=movie_id).first()
        if not movie:
            abort(404)

        try:
            movie.delete()

            return {
                "success": True,
                "id": movie_id
            }
        except Exception as e:
            print(e)
            abort(422)

    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        print(error.description)
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable" if 'message' not in error.description
                                        else error.description.get('message')
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

    return app


app = create_app()

if __name__ == '__main__':
    app.run()