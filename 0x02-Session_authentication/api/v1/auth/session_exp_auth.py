#!/usr/bin/env python3
""" Module Session Duration """
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ Class that inherits from SessionAuth
      that Exires Session Authentication  """

    def __init__(self):
        """ Instance attribute of session duration """
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a session with expiration details.

        Args:
            user_id (str):
                 The user ID for which the session is created.

        Returns:
            str: The session ID
            or None if session creation fails.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_data = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_data

        print(f"Created session: {session_data}")
        print(f"All the sessions: {self.user_id_by_session_id}")

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve user ID from
        session if it's not expired.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID or
            None if session is expired or invalid.
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        print(f"Expiration time: {expiration_time}")

        return session_dict.get("user_id")
