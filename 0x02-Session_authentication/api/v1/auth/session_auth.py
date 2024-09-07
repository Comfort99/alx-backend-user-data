#!/usr/bin/env python3
""" Session Authentication Model """
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ Class that inherits from Auth
    to authorize a Session
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session ID for a given user_id.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The generated session ID or None if user_id is invalid.
            """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID associated with the session ID,
            or None if not found.
          """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ doc doc """
        session_id = self.session_cookie(request=request)

        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id=session_id)

        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Destroys the user session /
        logs out the user.

    Args:
        request: The HTTP request object containing
        the session cookie.

    Returns:
        True if the session was successfully
        destroyed, otherwise False.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)

        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        if session_id in self.user_id_by_session_id:
            self.user_id_by_session_id.pop(session_id)
            return True

        return False
