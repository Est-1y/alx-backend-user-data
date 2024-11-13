#!/usr/bin/env python3
"""Auth
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Auth class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth func
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        normalized_path = path.rstrip('/')

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if normalized_path.startswith(excluded_path[:-1]):
                    return False
            elif normalized_path == excluded_path.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """getting authorization header"""

        if request is None:
            return None
        header_value = request.headers.get('Authorization', None)
        return header_value

    def current_user(self, request=None) -> TypeVar('User'):
        """getting the current user
        """
        return None

    def session_cookie(self, request=None):
        """getting cookie value
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')
        if session_name is None:
            return None

        return request.cookies.get(session_name)
