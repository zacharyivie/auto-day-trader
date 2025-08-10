import dearpygui.dearpygui as dpg

# Simple in-memory "session"
SESSION = {"authenticated": False, "username": None}

# Utility to show only one "page" window at a time
PAGES = ["page_login", "page_home", "page_settings"]
def navigate(to_page_id: str):
    for pid in PAGES:
        dpg.configure_item(pid, show=(pid == to_page_id))

# Callbacks
def on_login(sender, app_data, user_data):
    username = dpg.get_value("login_username")
    password = dpg.get_value("login_password")
    # TODO: integrate with your session_service.authenticate(username, password)
    if username and password:
        SESSION["authenticated"] = True
        SESSION["username"] = username
        dpg.set_value("home_welcome_text", f"Welcome, {username}!")
        navigate("page_home")
    else:
        dpg.configure_item("login_error_text", show=True)
        dpg.set_value("login_error_text", "Invalid username/password")

def on_logout(sender, app_data, user_data):
    SESSION["authenticated"] = False
    SESSION["username"] = None
    dpg.set_value("login_username", "")
    dpg.set_value("login_password", "")
    navigate("page_login")

def to_home(sender, app_data, user_data):
    if SESSION["authenticated"]:
        navigate("page_home")
    else:
        navigate("page_login")

def to_settings(sender, app_data, user_data):
    if SESSION["authenticated"]:
        navigate("page_settings")
    else:
        navigate("page_login")

def save_settings(sender, app_data, user_data):
    # Read settings values
    api_key = dpg.get_value("settings_api_key")
    risk = dpg.get_value("settings_risk")
    show_logs = dpg.get_value("settings_show_logs")
    # TODO: call into your services layer to persist securely (e.g., encrypt api_key, save to SQLite)
    print("Saved settings:", {"api_key": "(hidden)", "risk": risk, "show_logs": show_logs})
    dpg.configure_item("settings_toast", show=True)
    dpg.split_frame()  # small delay before hiding toast
    dpg.configure_item("settings_toast", show=False)

# App UI
dpg.create_context()
dpg.create_viewport(title="Auto Trader - Demo", width=840, height=520)

with dpg.window(tag="page_login", label="Login", width=800, height=480, no_move=True, no_resize=True, no_collapse=True):
    dpg.add_spacer(height=10)
    dpg.add_text("Sign in to Auto Trader", color=(200, 220, 255))
    dpg.add_separator()
    dpg.add_input_text(tag="login_username", label="Username", width=300)
    dpg.add_input_text(tag="login_password", label="Password", password=True, width=300)
    dpg.add_checkbox(tag="login_remember", label="Remember me")
    dpg.add_button(label="Login", callback=on_login)
    dpg.add_text(tag="login_error_text", default_value="", color=(255, 120, 120), show=False)

with dpg.window(tag="page_home", label="Home", width=800, height=480, no_move=True, no_resize=True, no_collapse=True, show=False):
    dpg.add_text(tag="home_welcome_text", default_value="Welcome!")
    dpg.add_separator()
    with dpg.group(horizontal=True):
        dpg.add_button(label="Settings", callback=to_settings)
        dpg.add_button(label="Logout", callback=on_logout)
    dpg.add_spacer(height=10)
    dpg.add_text("Dashboard")
    with dpg.group():
        dpg.add_text("• Status: Connected (demo)")
        dpg.add_text("• Open Positions: 0 (demo)")
        dpg.add_text("• PnL: $0.00 (demo)")

with dpg.window(tag="page_settings", label="Settings", width=800, height=480, no_move=True, no_resize=True, no_collapse=True, show=False):
    dpg.add_text("Settings")
    dpg.add_separator()
    dpg.add_input_text(tag="settings_api_key", label="Broker API Key", password=True, width=400)
    dpg.add_slider_float(tag="settings_risk", label="Risk % per trade", default_value=1.0, min_value=0.1, max_value=5.0, width=300)
    dpg.add_checkbox(tag="settings_show_logs", label="Show detailed logs", default_value=True)
    with dpg.group(horizontal=True):
        dpg.add_button(label="Save", callback=save_settings)
        dpg.add_button(label="Back", callback=to_home)
    dpg.add_text(tag="settings_toast", default_value="Settings saved!", color=(120, 220, 120), show=False)

# Menu bar (global)
with dpg.viewport_menu_bar():
    with dpg.menu(label="Navigate"):
        dpg.add_menu_item(label="Login", callback=lambda: navigate("page_login"))
        dpg.add_menu_item(label="Home", callback=to_home)
        dpg.add_menu_item(label="Settings", callback=to_settings)
    with dpg.menu(label="Session"):
        dpg.add_menu_item(label="Logout", callback=on_logout)

dpg.setup_dearpygui()
dpg.show_viewport()
navigate("page_login")
dpg.start_dearpygui()
dpg.destroy_context()