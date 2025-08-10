from .tags import WINDOW_TAGS
import dearpygui.dearpygui as dpg

def navigate(to_window: str):
    for tag in WINDOW_TAGS:
        dpg.hide_item(tag)
    dpg.show_item(to_window)
    dpg.set_primary_window(to_window, True)