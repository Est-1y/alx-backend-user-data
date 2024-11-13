#!/usr/bin/env python3

""" Flask View module,
"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def auth_login_session():
    """ POST /api/v1/auth_session/login,,
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 400
    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 400

        from api.v1.app import auth  # to avoid circular import
        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        session_name = getenv("SESSION_NAME")  # set the session cookie name
        response.set_cookie(session_name, session_id)

        return response
    return jsonify({"error:" "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def handle_logout():
    """
    user logout
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
