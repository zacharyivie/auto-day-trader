import dearpygui.dearpygui as dpg

def settings_window():
    with dpg.window(label="settings", tag="settings_window", no_move=True, no_resize=True, no_collapse=True, no_title_bar=True, no_close=True) as window:
        dpg.add_text("Settings")