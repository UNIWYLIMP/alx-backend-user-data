#!/usr/bin/env python3
""" Authentication Implementation modules."""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Initialize the auth."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user already exists with the passed email.
        """
        try:
            self._db.find_user_by(email=email)
        except:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))
