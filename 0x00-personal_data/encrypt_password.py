#!/usr/bin/env python3
""" Password Encryption and Validation """
import bcrypt


def hash_password(password: str) -> bytes:
    """ Passwords are essential for user authentication """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ we must store them securely to prevent unauthorized access """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
