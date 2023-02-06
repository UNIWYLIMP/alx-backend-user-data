#!/usr/bin/env python3
""" Basic Auth."""
from api.v1.auth.auth import Auth
from models.user import User
import base64
import binascii
from typing import TypeVar


UserType = TypeVar('User', bound=User)


class BasicAuth(Auth):
    """ Defines basic authentication."""
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """ Implements base64 part of Base."""
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split("Basic ")[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """ Decodes the base64 autherization header."""
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            decoded = base64.b64decode(
                    base64_authorization_header).decode('utf-8')
        except (UnicodeDecodeError, binascii.Error):
            return None

        return decoded

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """ Extract the user credentials."""
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None
        parts = decoded_base64_authorization_header.split(":", 1)
        if len(parts) != 2:
            return None, None
        email, password = parts

        return email, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> UserType:
        """ User object from credentials."""
        if user_email is None or not isinstance(user_email, str)\
                or user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overlaods the current user."""
        auth_header = request.headers.get('Authorization')
        base64_auth_header = self.extract_base64_authorization_header(
                auth_header)

        decoded_base64_auth_header = self.decode_base64_authorization_header(
                base64_auth_header)
        user_email, user_pwd = self.extract_user_credentials(
                decoded_base64_auth_header)

        return self.user_object_from_credentials(user_email, user_pwd)
