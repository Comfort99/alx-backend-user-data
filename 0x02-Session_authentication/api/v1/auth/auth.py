#!/usr/bin/env python3
""" Authentication Module """
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ Class to manage the API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if authentication is required
        based on the path and excluded paths.

        Args:
            path (str): The path to be checked.
            excluded_paths (List[str]):
            A list of paths that do not require authentication.
        Returns:
            bool"""
        if path is None:
            return True
        if not excluded_paths:
            return True

        path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            if excluded_path == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Retrieves the authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: None, since this will be implemented later. """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the current user based on the request.

        Args:
            request: The Flask request object."""
        return None

    def session_cookie(self, request=None):
        """ Returns the value of the session cookie from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: The value of the session cookie, or None if not found.
            """
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME", "_my_session_id")

        return request.cookies.get(session_name)
