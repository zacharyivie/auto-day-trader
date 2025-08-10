import dearpygui.dearpygui as dpg
from .core.routing import navigate
from .pages import register_pages

def run_app():
    dpg.create_context()
    
    register_pages()
    
    navigate("login_window")
    navigate("settings_window")
    
    dpg.create_viewport(title='Auto Day Trader', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
    
if __name__ == "__main__":
    run_app()
