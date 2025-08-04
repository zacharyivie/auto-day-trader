from threading import Lock
from cryptography.fernet import Fernet
from logging import Logger, getLogger

_LOGGER_NAME: str = __name__.split('.')[-1].upper()

class SessionService:
    _instance: "SessionService | None" = None
    _lock: Lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self._user_id: int | None = None
            self._username: str | None = None
            self._encryption_key: str | None = None
            self._fernet: Fernet | None = None
            self.initialized: bool = True
            self._logger: Logger = getLogger(_LOGGER_NAME)
            
    def login(self, user_id: int, username: str, encryption_key: str) -> None:
        self._user_id = user_id
        self._username = username
        self._encryption_key = encryption_key
        self._fernet = Fernet(encryption_key)
        self._logger.info(f"User {user_id} session started successfully.")
        
    def logout(self) -> None:
        self._user_id = None
        self._username = None
        self._encryption_key = None
        self._fernet = None
        self._logger.info("User session ended successfully.")
        
    @property
    def user_id(self) -> int | None:
        return self._user_id
    
    @property
    def username(self) -> str | None:
        return self._username
    
    @property
    def encryption_key(self) -> str | None:
        return self._encryption_key
    
    @property
    def fernet(self) -> Fernet | None:
        return self._fernet
    
    def encrypt(self, data: str) -> str:
        if not self._fernet:
            raise ValueError("Fernet instance not initialized")
        return self._fernet.encrypt(data.encode()).decode()
    
    def decrypt(self, data: str) -> str:
        if not self._fernet:
            raise ValueError("Fernet instance not initialized")
        return self._fernet.decrypt(data.encode()).decode()
    
session = SessionService()