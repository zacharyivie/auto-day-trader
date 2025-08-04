import logging
import re

from .user_service import UserService
from backend.security import verify_password
from backend.security import derive_encryption_key
from .session_service import SessionService

_LOGGER_NAME: str = __name__.split('.')[-1].upper()
session: SessionService = SessionService()    

class AuthService:
    def __init__(self):
        self._logger: logging.Logger = logging.getLogger(_LOGGER_NAME)
        self._user_service: UserService = UserService()
        
    def login(self, username: str, password: str) -> bool:
        if session.user_id is not None:
            self._logger.error("Unable to login - User already logged in")
            return False
        user_id = self._user_service.GetUserIdByUsername(username=username)
        if user_id is None:
            self._logger.info(f"User with username {username} does not exist")
            return False
        user_info = self._user_service.GetUserById(id=user_id)
        if user_info is None:
            self._logger.info(f"No user with id {user_id} exists")
            return False
        salt: str = user_info['salt']
        password_hash: str = user_info['password']
        if verify_password(password=password, password_hash=password_hash, salt=salt):
            encryption_key = derive_encryption_key(password=password, salt=salt, context="AutoDayTrader_Encryption")
            session.login(user_id=user_id, username=username, encryption_key=encryption_key)
            self._logger.info(f"User {user_id} logged in successfully")
            return True
        self._logger.info(f"User {user_id} failed to log in")
        return False
    
    def signup(self, username: str, password: str) -> bool:
        if not self._validate_username(username):
            self._logger.info("Username is invalid")
            return False
        if not password:
            self._logger.info("Password is empty")
            return False
        if not self._validate_password(password=password):
            self._logger.info("Password is invalid")
            return False
        if self._user_service.CreateUser(username=username, password=password):
            self._logger.info(f"User \"{username}\" created successfully. Logging in...")
            return self.login(username=username, password=password)
        self._logger.info(f"Failed to create user \"{username}\"")
        return False
        
    def _validate_username(self, username: str) -> bool:
        if not username:
            return False
        valid = r'^[a-zA-Z0-9]{3,25}$'
        return bool(re.match(valid, username))

    def _validate_password(self, password: str) -> bool:
        if not password:
            return False
        if not bool(len(password) >= 8 and len(password) <= 25):
            self._logger.info("Password is invalid length")            
            return False
        if not re.search(r'[A-Z]', password):
            self._logger.info("Password is missing an uppercase letter")
            return False
        if not re.search(r'[a-z]', password):
            self._logger.info("Password is missing a lowercase letter")
            return False
        if not re.search(r'[0-9]', password):
            self._logger.info("Password is missing a number")
            return False
        if not re.search(r'[^\w]', password):
            self._logger.info("Password is missing a special character")
            return False
        return True