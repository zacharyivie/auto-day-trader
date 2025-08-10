from .login import create_login_window
from .signup import create_sign_up_window
from .home import home_window
from .settings import settings_window

def register_pages():
    create_login_window()
    create_sign_up_window()
    home_window()
    settings_window()