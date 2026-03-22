import customtkinter as ctk
from DB import CRUD
from CTkMessagebox import CTkMessagebox


class BestsFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

case "bests":
                # TODO: implement bests frame with statistics like most points, most consistent player, etc.
                self._current_frame = "bests"
                self.stats_frame.grid(row=0, column=1, sticky="nsew")
                self.stats_frame.grid_rowconfigure((0, 1), weight=1)  # type: ignore