from backend.users import User
from sqlite3 import IntegrityError
import logging
from backend.security import hash_and_salt

_LOGGER_NAME: str = __name__.split('.')[-1].upper()

class UserService:
    def __init__(self):
        self._user: User = User()
        self._logger: logging.Logger = logging.getLogger(_LOGGER_NAME)
        
    def CreateUser(self, username: str, password: str) -> bool:
        """Attempt new user creation with username and password, returns True on success, False on failure"""
        try:
            password_hash, salt = hash_and_salt(password)
            self._user.CreateUser(username=username, password=password_hash, salt=salt)
            self._logger.info(f"Created user with username {username}")
            return True
        except IntegrityError as e:
            if "username" in str(e):
                self._logger.error(f'Username "{username}" already exists or is invalid')
            if "password" in str(e):
                self._logger.error(f'Password "{password}" is invalid')
            return False
        except Exception as e: # something went wrong in db communication
            self._logger.error(f"Database communication error - Failed to create a user with username {username}: {e}")
            return False
        
    def DeleteUserById(self, id: int) -> bool:
        try: # happy path, results in no user with id=id in db
            num_deleted: int = self._user.DeleteUser(id=id)
            if num_deleted == 0:
                self._logger.error(f"User with id {id} does not exist to delete")
            elif num_deleted > 1:
                self._logger.error(f"DANGER: Multiple users deleted with id {id}")
            else:
                self._logger.info(f"Deleted user with id {id}")
            return True
        except Exception as e: # error communicating with db
            self._logger.error(f"Database communication error - Failed to delete a user with id {id}: {e}")
            return False
        
    def GetUserById(self, id: int) -> dict[str, str] | None:
        try:
            user: dict[str, str] = self._user.GetUserById(id=id)
            self._logger.info(f"Retrieved user data for id {id}")
            return user
        except ValueError as e:
            self._logger.error(e)
        except Exception as e:
            self._logger.error(f"Database communication error - Failed to get a user with id {id}: {e}")
            
    def GetUserIdByUsername(self, username: str) -> int | None:
        try:
            user_id: dict[str, int] = self._user.GetUserIdByUsername(username=username)
            self._logger.info(f"Retrieved user id for username \"{username}\"")
            return user_id['id']
        except ValueError as e:
            self._logger.error(e)
        except Exception as e:
            self._logger.error(f"Database communication error - Failed to get a user with username \"{username}\": {e}")