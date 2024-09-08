#!/usr/bin/env python3
""" Module Login Session Authentication """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def Login():
    """ Handles the login
    POST /auth_session/login route for
    session authentication.

    Returns:
        JSON response containing user
        information or error messages.
        """
    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user_credentials = User.search({"email": email})
    if not user_credentials or len(user_credentials) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = user_credentials[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # creates a session for the given user id
    session_id = auth.create_session(user.id)

    # internal server error
    if not session_id:
        abort(500)

    response = jsonify(user.to_json())

    session_name = getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def LogOut():
    """ DELETE /auth_session/logout
        Return:
            - Empty dictionary if succesful
            """
    from api.v1.app import auth

    deleted = auth.destroy_session(request)

    if not deleted:
        abort(404)

    return jsonify({}), 200
