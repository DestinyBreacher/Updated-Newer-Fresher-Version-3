import pathlib

import dearpygui.dearpygui as dpg

from Application import Image

from .bill import BillingWindow


class ImageWindow:
    def __init__(self, folder: pathlib.Path, cam: str, parent):
        # List of things the image window knows about:
        # 1. The roll that is currently being billed
        # 2. The images in the roll
        # 3. A BilledWindow

        # What does the ImageWindow do?
        # 1. Creates and manages the BilledWindow
        # 2. Lets us open our image of choice
        # 3. Has a preview for the next and previous image

        self.folder = folder
        self.current_image: int = 1
        self.billing_window = BillingWindow(cam, folder.name)
        self.setup(parent)

    def setup(self, parent):
        with dpg.child_window(parent=parent):
            image1 = list(self.folder.iterdir())[0]
            width, height, channel, data = Image.frompath(image1).dpg_texture
            with dpg.texture_registry(show=True):
                dpg.add_static_texture(
                    width=width, height=height, default_value=data, tag="Main Image"
                )
            dpg.add_image("Main Image")

    def open(self, index: int):
        pass

    def next(self):
        next_image = self.current_image + 1
        self.open(next_image)
        self.billing_window.load(next_image)

    def previous(self):
        previous_image = self.current_image - 1
        self.open(previous_image)
        self.billing_window.load(previous_image)