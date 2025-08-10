import dearpygui.dearpygui as dpg

def home_window():
    with dpg.window(label="Home", tag="home_window", no_move=True, no_resize=True, no_collapse=True, no_title_bar=True, no_close=True):
        dpg.add_text("Home")