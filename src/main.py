from frontend import run_app
from dotenv import load_dotenv
from services import UserService, setup_logging, AuthService, SessionService

_ = load_dotenv()
setup_logging()
session = SessionService()

def print_exit_status(exit_code: int):
    session.logout()
    if exit_code == 0:
        print("Application exited successfully.")
    else:
        print(f"Application exited with error code {exit_code}.")

def run() -> None:
    user_service = UserService()
    auth_service = AuthService()
    _ = auth_service.signup(username="testuser15", password="Password123!")
    _ = auth_service.login(username="testuser15", password="Password123!")
    user_id = user_service.GetUserIdByUsername(username="testuser15")
    print(user_id)
    assert(user_id is not None)
    user_info = user_service.GetUserById(id=user_id)
    print(user_info)
    #_ = user_service.DeleteUserById(id=user_id)
    #print(user_service.GetUser(id=1))
    #user_service.DeleteUser(id=1)
    encrypted_data: str = session.encrypt(data="Hello world")
    print("Encrypted:", encrypted_data)
    decrypted_data: str = session.decrypt(data=encrypted_data)
    print("Decrypted:", decrypted_data)
    run_app()

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        session.logout()
        print("Application exited successfully.")