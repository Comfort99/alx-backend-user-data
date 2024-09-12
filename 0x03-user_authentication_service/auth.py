#!/usr/bin/env python3
""" Authentication Model """
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    """ A method to encrypt a password """
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password


def _generate_uuid() -> str:
    """ Return a string representation of a new UUID """
    UUID = str(uuid4())
    return UUID


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ A function that takes email and password
         and registers the user to the database
          with their encrypted password """

        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exist")
        except NoResultFound:
            passwd_hashed = _hash_password(password)

            new_user = self._db.add_user(
                email=email, hashed_password=passwd_hashed)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ A function that validates that every login user
         is valid hashed password"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        hashed_password = user.hashed_password

        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def create_session(self, email: str) -> str:
        """ A fuction that creates a login a unique
        session_id and set it as a cookie """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()

        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ A function that returns a respective user by a session_id """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: str) -> None:
        """ A function that takes a user_id and deletes a
         session_id which enables a user to log_out
          on the end point """
        if user_id is None:
            return None

        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        self._db.update_user(user.id, session_id=None)

        return None

    def get_reset_password_token(self, email: str) -> str:
        """ A function that takes an email
         and create a unique token which enables the
          user to uodate their password """
        if email is None:
            return None

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ A function that takes a generated token
         and choosen password and update it in
          the database """
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password=password)

        self._db.update_user(user_id=user.id,
                             hashed_password=hashed_password,
                             reset_token=None)
