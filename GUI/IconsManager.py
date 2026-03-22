import customtkinter as ctk
from PIL import Image, ImageTk
import os


class IconRegistry:
    def __init__(self, base_path="GUI/Assets/Icons", default_size=(30, 30)):
        self.base_path = base_path
        self.default_size = default_size
        self._cache = {}

    def _load_icon(self, name, size):
        key = (name, size)
        if key in self._cache:
            return self._cache[key]

        light_path = os.path.join(self.base_path, "light", f"{name}.png")
        dark_path = os.path.join(self.base_path, "dark", f"{name}.png")

        light_exist = os.path.exists(light_path)
        dark_exist = os.path.exists(dark_path)

        if not light_exist and not dark_exist:
            raise FileNotFoundError(f"Icon '{name}' not found in light/ or dark/ folders")

        if light_exist:
            light_img = Image.open(light_path)
        else:
            light_img = None

        if dark_exist:
            dark_img = Image.open(dark_path)
        else:
            dark_img = None

        # fallback
        if light_img is None:
            light_img = dark_img

        if dark_img is None:
            dark_img = light_img

        icon = ctk.CTkImage(
            light_image=light_img,
            dark_image=dark_img,
            size=size
        )

        self._cache[key] = icon
        return icon

    def __getattr__(self, name):
        return self._load_icon(name, self.default_size)

    def get(self, name, size):
        return self._load_icon(name, size)


icons = IconRegistry()
