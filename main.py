import logging
from pathlib import Path

import dearpygui.dearpygui as dpg

import Application
import GUI

logger = logging.getLogger("Core.Main")


def make_image_window(path: Path):
    with dpg.window(width=1035, height=608) as image_window:
        image_manager = Application.ImageManager(
            mode="offline", roll=path.name, path=path
        )
        billing_window = GUI.BillingWindow(roll="30R", path=path)
        GUI.ImageWindow(image_window, billing_window, image_manager)


def load_image_folder(sender, app_data, user_data):
    path = Path(app_data["file_path_name"])
    make_image_window(path)


def load_mess_list(sender, app_data, user_data):
    # yuck
    path = next(iter(app_data["selections"].values()))
    path = Path(path)
    Application.db.read_mess_list(path)
    GUI.modal_message("Mess list loaded successfully!")


def main():
    dpg.create_context()
    dpg.create_viewport(title="DoPy")
    core_logger = logging.getLogger("Core")
    gui_logger = logging.getLogger("GUI")
    core_logger.setLevel(logging.DEBUG)
    gui_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[{threadName}][{asctime}] [{levelname:<8}] {name}: {message}",
        "%H:%M:%S",
        style="{",
    )
    with dpg.window(tag="Primary Window"):
        with dpg.file_dialog(
            directory_selector=False,
            show=False,
            tag="mess_list_file_dialog",
            callback=load_mess_list,
            height=400,
        ):
            dpg.add_file_extension(".csv", color=(0, 255, 0, 255), custom_text="[CSV]")

        dpg.add_file_dialog(
            directory_selector=True,
            show=False,
            tag="roll_folder_dialog",
            callback=load_image_folder,
            height=400,
        )

        with dpg.menu_bar():
            with dpg.menu(label="Tools"):
                dpg.add_menu_item(
                    label="Load Roll",
                    callback=lambda: dpg.show_item("roll_folder_dialog"),
                )
                dpg.add_menu_item(
                    label="Load Mess List",
                    callback=lambda: dpg.show_item("mess_list_file_dialog"),
                )
                dpg.add_menu_item(
                    label="Show Performance Metrics", callback=dpg.show_metrics
                )

            dpg.add_button(
                label="Music",
                callback=lambda: GUI.MusicVisualiser(
                    "./Data/Audio/clodman.mp3"
                ).start(),
            )
    with dpg.window(height=350, width=350, label="Logger") as logger_window:
        log = GUI.Logger(parent=logger_window)
        log.setFormatter(formatter)
        core_logger.addHandler(log)
        gui_logger.addHandler(log)
    dpg.setup_dearpygui()
    dpg.set_primary_window("Primary Window", True)
    dpg.set_viewport_vsync(False)
    dpg.show_viewport(maximized=True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
