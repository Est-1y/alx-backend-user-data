#!/usr/bin/env python3
""" Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def authorized() -> str:
    """ Getting unauthorized
    """
    abort(401, description="Unauthorized")


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbid() -> str:
    """ Getting forbidden
    """
    abort(403, description="Forbidden")


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ Getting status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ Getting stats
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)
