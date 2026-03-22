import os
import datetime
import customtkinter as ctk

from CTkMessagebox import CTkMessagebox
from GUI.IconsManager import icons

import supporting_functions as sf
from GUI.Frames.HomeWindow import HomeFrame
from GUI.Frames.PlayersWindow import PlayersFrame
# from GUI.Frames.GamesWindow import GamesFrame
# from GUI.Frames.StatsWindow import StatsFrame
# from GUI.Frames.BestsWindow import BestsFrame
# from GUI.Frames.TempGameWindow import TempGameFrame
from DB import CRUD


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # set window title and size
        self.title("7_cudów_świata.py")
        self.geometry("1400x700")

        # set window grid to 1x2 (row x column)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # set appearance mode
        ctk.set_appearance_mode("System")

        # load players and games from database
        self._games = CRUD.get_all_games()

        # list of players from last game (instance only, not loaded from database)
        self._last_game = []

        # dynamic buttons/menus/labels/checkboxes
        self._active_player_menus_list = []
        self._game_view_buttons = []
        self._game_delete_buttons = []
        self._player_chekboxes = []
        self._players_chekboxes = []

        # frame tracking
        self._current_frame = "home"

        # game_id from game creation to be used in game details CRUD saving
        self._latest_game_id = None

        # flags
        self._empty_game_present_flag = False
        self._game_properly_calculated_flag = False
        self._player_editing_flag = False

        # icon loading
        # navigation icons
        # image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Assets/Icons/Dark")
        # self.players_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "User.png")),
        #                                   dark_image=Image.open(os.path.join(image_path, "User_Stats.png")),
        #                                   size=(30, 30))
        # self.games_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "Games.png")),
        #                                 dark_image=Image.open(os.path.join(image_path, "Games.png")),
        #                                 size=(30, 30))
        # self.stats_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "Stats.png")),
        #                                 dark_image=Image.open(os.path.join(image_path, "Stats.png")),
        #                                 size=(30, 30))
        # self.game_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "Game.png")),
        #                                dark_image=Image.open(os.path.join(image_path, "Game.png")),
        #                                size=(30, 30))
        # self.trophy_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "Trophy.png")),
        #                                  dark_image=Image.open(os.path.join(image_path, "Trophy.png")),
        #                                  size=(30, 30))
        #
        # # reusable icons
        # self.add_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "Add.png")),
        #                               size=(20, 20))
        # self.delete_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "Delete.png")),
        #                                  size=(20, 20))
        # self.duplicate_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "Duplicate.png")),
        #                                     size=(20, 20))
        # self.save_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "Save.png")),
        #                                size=(30, 30))
        # self.calculate_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "Calculate.png")),
        #                                     size=(30, 30))
        # self.cancel_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "Cancel.png")),
        #                                  size=(30, 30))
        # self.edit_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "Edit.png")),
        #                                size=(20, 20))
        # self.view_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "View.png")),
        #                                size=(20, 20))
        #
        # # home icons
        # self.add_player_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "Add_user.png")),
        #                                      size=(100, 100))
        # self.add_game_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "Add_game.png")),
        #                                    size=(100, 100))
        #
        # # stats icons
        # self.user_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "User_Stats.png")),
        #                                size=(100, 100))
        # self.users_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "Users.png")),
        #                                 size=(100, 100))

        # navigation frame
        self.nav_frame = ctk.CTkFrame(self, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="nsew")
        self.nav_frame.grid_rowconfigure(6, weight=1)

        self.nav_buttons = {}
        self.nav_buttons["HomeFrame"] = ctk.CTkButton(self.nav_frame, corner_radius=0, height=40, border_spacing=10,
                                                      text="Home", fg_color=("gray75", "gray25"),
                                                      text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=icons.Home, anchor="w", font=ctk.CTkFont(size=15),
                                                      command=lambda: self.show_frame("HomeFrame"))
        self.nav_buttons["HomeFrame"].grid(row=0, column=0, sticky="ew")

        self.nav_buttons["PlayersFrame"] = ctk.CTkButton(self.nav_frame, corner_radius=0, height=40, border_spacing=10,
                                                         text="Players", fg_color="transparent",
                                                         text_color=("gray10", "gray90"),
                                                         hover_color=("gray70", "gray30"), image=icons.Users,
                                                         anchor="w", font=ctk.CTkFont(size=15),
                                                         command=lambda: self.show_frame("PlayersFrame"))
        self.nav_buttons["PlayersFrame"].grid(row=1, column=0, sticky="ew")

        self.nav_buttons["GamesFrame"] = ctk.CTkButton(self.nav_frame, corner_radius=0, height=40, border_spacing=10,
                                                       text="Games", fg_color="transparent",
                                                       text_color=("gray10", "gray90"),
                                                       hover_color=("gray70", "gray30"), image=icons.Games, anchor="w",
                                                       command=lambda: self.show_frame("GamesFrame"),
                                                       font=ctk.CTkFont(size=15))
        self.nav_buttons["GamesFrame"].grid(row=2, column=0, sticky="ew")

        self.nav_buttons["StatsFrame"] = ctk.CTkButton(self.nav_frame, corner_radius=0, height=40, border_spacing=10,
                                                       text="Statistics", fg_color="transparent",
                                                       text_color=("gray10", "gray90"),
                                                       hover_color=("gray70", "gray30"), image=icons.Stats, anchor="w",
                                                       command=lambda: self.show_frame("StatsFrame"),
                                                       font=ctk.CTkFont(size=15))
        self.nav_buttons["StatsFrame"].grid(row=3, column=0, sticky="ew")

        self.nav_buttons["TrophyFrame"] = ctk.CTkButton(self.nav_frame, corner_radius=0, height=40, border_spacing=10,
                                                        text="Bests", fg_color="transparent",
                                                        text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"), image=icons.Trophy,
                                                        anchor="w",
                                                        command=lambda: self.show_frame("TrophyFrame"),
                                                        font=ctk.CTkFont(size=15))
        self.nav_buttons["TrophyFrame"].grid(row=4, column=0, sticky="ew")

        self.nav_buttons["TemporaryGameFrame"] = ctk.CTkButton(self.nav_frame, corner_radius=0, height=40,
                                                               border_spacing=10, text="Game (Temporary)",
                                                               fg_color="transparent", text_color=("gray10", "gray90"),
                                                               hover_color=("gray70", "gray30"), image=icons.Game,
                                                               anchor="w",
                                                               command=lambda: self.show_frame("TemporaryGameFrame"),
                                                               font=ctk.CTkFont(size=15))

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.nav_frame, values=["System", "Dark", "Light"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=20, sticky="s")

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # GamesFrame, StatsFrame, BestsFrame, TempGameFrame
        for F in (HomeFrame, PlayersFrame):
            frame = F(self.container, self, corner_radius=20)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomeFrame")

    # navigation buttons events
    def show_frame(self, frame_name: str) -> None:
        """
        Selects frame to display based on the name provided

        :param frame_name: String with the name of the frame to display, provided by the button event
        :return: None
        """

        # clear all dynamically created buttons/menus/labels
        self._active_player_menus_list = []

        self._game_view_buttons = []
        self._game_delete_buttons = []
        self._player_chekboxes = []
        self._players_chekboxes = []

        # clear temporary game frame button
        self.nav_buttons["TemporaryGameFrame"].grid_forget()

        # reset flags
        self._game_properly_calculated_flag = False

        # check for empty game and clear it if found
        if self._current_frame == "game" and self._empty_game_present_flag:
            CRUD.delete_last_game()
            self._empty_game_present_flag = False
            self._latest_game_id = None

        if self._player_editing_flag:
            CTkMessagebox(title="Warning", message="Save or cancel player edition before changing the frame",
                          icon="warning")
            return

        frame = self.frames[frame_name]

        if hasattr(frame, "refresh"):
            frame.refresh()
        frame.tkraise()

        for name, btn in self.nav_buttons.items():
            if name == frame_name:
                btn.configure(fg_color=("grey75", "grey25"))
            else:
                btn.configure(fg_color="transparent")

    def on_close(self) -> None:
        """
        Event for the window close button,
        checks if there are unsaved changes and asks for confirmation

        :return: None
        """
        if self._current_frame == "game" and self._empty_game_present_flag:
            quit_var = CTkMessagebox(title="Warning",
                                     message="You have unsaved game details, are you sure you want to quit?",
                                     icon="question", option_1="Save and quit", option_2="Quit without saving",
                                     corner_radius=10, sound=True, justify="center", option_focus=1)
            response = quit_var.get()

            if response == "Save and quit":
                if self.save_game_details_button_event():
                    self.quit()
            else:
                CRUD.delete_last_game()
                self.quit()
        elif self._current_frame == "players" and self._player_editing_flag:
            quit_var = CTkMessagebox(title="Warning",
                                     message="You have unsaved player details, are you sure you want to quit?",
                                     icon="question", corner_radius=10, sound=True, justify="center",
                                     option_1="Cancel", option_2="Quit anyway")
            response = quit_var.get()
            if response == "Quit anyway":
                self.quit()
        else:
            self.quit()

    # static methods
    @staticmethod
    def clear_frame(frame: ctk.CTkFrame | ctk.CTkScrollableFrame) -> None:
        """
        Clears the frame of all widgets, used to prepare the frame for new widgets

        :param frame: Frame to clear
        :return: None
        """
        for widget in frame.winfo_children():
            widget.destroy()

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str) -> None:
        """
        Changes the appearance mode of the app, from the list of "light", "dark" and "system"

        :param new_appearance_mode: String with the name of new appearance mode
        :return: None
        """
        ctk.set_appearance_mode(new_appearance_mode)
