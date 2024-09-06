#!/usr/bin/env python3
""" Basic Authorization Model """
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic Authorization class that inherits from Auth """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extracts the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header string.

        Returns:
            str: The Base64 part of the Authorization header,
            or None if invalid. """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        # Extract and return the Base64 part (after 'Basic ')
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ Decodes a Base64 string to a UTF-8 string.

        Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            str: The decoded UTF-8 string, or None if decoding fails.
            """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ doc doc """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        separater_index = decoded_base64_authorization_header.find(':')

        if separater_index == -1:
            return None, None

        email = decoded_base64_authorization_header[:separater_index]
        password = decoded_base64_authorization_header[separater_index + 1:]

        return email, password

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """ Returns the User instance based on email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            Optional[TypeVar('User')]:
                  The User instance or None if credentials are invalid.
                  """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            user_credentials = User.search({"email": user_email})
        except Exception:
            return None

        for user in user_credentials:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ doc doc """

        auth_header = self.authorization_header(request)

        if not auth_header:
            return None

        encode = self.extract_base64_authorization_header(auth_header)

        if not encode:
            return None

        decode = self.decode_base64_authorization_header(encode)

        if not decode:
            return None

        email, password = self.extract_user_credentials(decode)

        if not email or not password:
            return None

        user_credentials = self.user_object_from_credentials(email, password)

        return user_credentials
