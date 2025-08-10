import dearpygui.dearpygui as dpg

def create_login_window():
    with dpg.window(label="Login", tag="login_window", no_move=True, no_resize=True, no_collapse=True, no_title_bar=True, no_close=True):
        dpg.add_text("Login")
        dpg.add_input_text(label="Username")
        dpg.add_input_text(label="Password", password=True)
        dpg.add_button(label="Login")