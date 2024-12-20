#!/usr/bin/env python3

"""
SessionDButh
"""

from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth
    """

    def create_session(self, user_id=None):
        """
        Creating a Session ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kw = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**kw)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """user_id_for_session_id
        """
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id
        return None

    def destroy_session(self, request=None):
        """
        Destroying Session
        """
        if request is None:
            return False

        # Get the session ID from the request cookie
        session_id = self.session_cookie(request)

        if not session_id:
            return False

        # Search for the UserSession instance with the given session ID
        user_session = UserSession.search({"session_id": session_id})

        if user_session:
            # Remove the UserSession instance from the database
            user_session[0].remove()
            return True

        return False
