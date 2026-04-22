#!/usr/bin/env python3
"""DB module for the user authentication service"""
import uuid
import bcrypt
from db import DB
from user import User
from bcrypt import hashpw, gensalt
from sqlalchemy.orm.exc import NoResultFound


def _generate_uuid() -> str:
    """Return a string representation of a new UUID."""
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """hashed password"""
    return hashpw(password.encode(), gensalt())


class Auth:
    """Auth class to interact with auth data"""

    def __init__(self):
        """initialize auth class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user to the database"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login credentials."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode("utf-8"),
                              user.hashed_password)

    def create_session(self, email: str) -> str:
        """Create a session for the user and return the session ID."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
