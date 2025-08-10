import dearpygui.dearpygui as dpg

def create_sign_up_window():
    with dpg.window(label="Sign Up", tag="sign_up_window", no_move=True, no_resize=True, no_collapse=True, no_title_bar=True, no_close=True):
        dpg.add_text("Sign Up")
        dpg.add_input_text(label="Username")
        dpg.add_input_text(label="Password", password=True)
        dpg.add_button(label="Sign Up")