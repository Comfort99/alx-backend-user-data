#!/usr/bin/env python3
""" Authentication Module """
from flask import request
from typing import List, TypeVar


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
        if not excluded_paths or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
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
