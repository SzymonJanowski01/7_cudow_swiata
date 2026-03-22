import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from DB import CRUD
from GUI.IconsManager import icons


class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)

        self.controller = controller
        self._players = CRUD.get_all_users()
        self._active_player_menus_list = []

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)  # type: ignore
        # self.add_game_button_event()

        home_frame_add_player_button = ctk.CTkButton(self, text="Add player", compound="top",
                                                     height=200, width=200, image=icons.get("Add_user", (100, 100)),
                                                     text_color="black", font=ctk.CTkFont(size=20),
                                                     command=self.add_player_button_event)
        home_frame_add_player_button.grid(row=0, column=0, padx=20, pady=20)

        home_frame_add_game_button = ctk.CTkButton(self, text="Add game", compound="top", height=200,
                                                   width=200, image=icons.get("Add_game", (100, 100)),
                                                   text_color="black", font=ctk.CTkFont(size=20),
                                                   command=self.add_game_button_event)
        home_frame_add_game_button.grid(row=1, column=0, padx=20, pady=20)

        # home_buttons frame
        self.home_buttons_frame = ctk.CTkFrame(self, corner_radius=50, fg_color="transparent", border_color="grey50",
                                               border_width=2)
        self.home_buttons_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        self.home_buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)  # type: ignore
        self.home_buttons_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)  # type: ignore

    def add_player_button_event(self) -> None:
        """
        Event for the add player button in the home frame,
        creates a new player entry in the database

        :return: None
        """
        add_player_label = ctk.CTkLabel(self.home_buttons_frame, text="Add player", font=ctk.CTkFont(size=30))
        add_player_label.grid(row=0, column=1, padx=20, pady=20)
        self.add_player_input = ctk.CTkEntry(self.home_buttons_frame, font=ctk.CTkFont(size=20),
                                             placeholder_text="New player name", width=200, height=50)
        self.add_player_input.grid(row=1, column=1, padx=20, pady=20)
        add_player_button = ctk.CTkButton(self.home_buttons_frame, text="", fg_color="green", hover_color="darkgreen",
                                          image=icons.Save, height=35, font=ctk.CTkFont(size=20),
                                          command=self.save_new_player_button_event)
        add_player_button.grid(row=2, column=1, padx=20, pady=20)

    def save_new_player_button_event(self) -> None:
        """
        Event for the save new player button in the home frame,
        saves the player to the database or displays an error message
        :return: None
        """
        username = self.add_player_input.get()
        result = CRUD.create_user(username)
        if result:
            # update players list for correct players list frame display
            self._players = CRUD.get_all_users()
            self.add_player_input.delete(0, "end")

            success_entry = ctk.CTkEntry(self.home_buttons_frame, font=ctk.CTkFont(size=20), fg_color="transparent",
                                         border_width=5, border_color="green", width=400, height=50)
            success_entry.insert(0, f"User {username} added successfully")
            success_entry.configure(state="disabled", justify="center")
            success_entry.grid(row=3, column=1, padx=20, pady=20)
            success_entry.after(1500, success_entry.destroy)
        elif result is False:
            error_entry = ctk.CTkEntry(self.home_buttons_frame, font=ctk.CTkFont(size=20), fg_color="transparent",
                                       border_width=5, border_color="#BF2A2A", width=400, height=50)
            error_entry.insert(0, f"Error while adding user {username}")
            error_entry.configure(state="disabled", justify="center")
            error_entry.grid(row=3, column=1, padx=20, pady=20)
            error_entry.after(1500, error_entry.destroy)
        else:
            # if result is None (no connection to database) shutdown the app
            self.quit()

    def add_game_button_event(self) -> None:
        """
        Event for the add game button in the home frame,
        creates a new game entry in the database

        :return: None
        """
        self._active_player_menus_list = []
        # convert list of tuples to list of strings for option menus
        self.potential_players = [player[0] for player in self._players]

        add_game_label = ctk.CTkLabel(self.home_buttons_frame, text="Add game", font=ctk.CTkFont(size=30))
        add_game_label.grid(row=0, column=1, padx=10, pady=10)

        # add/delete players option menu, or duplicate the last saved player line-up
        add_more_players_to_game_button = ctk.CTkButton(self.home_buttons_frame, text="", fg_color="green",
                                                        hover_color="darkgreen", image=icons.Add,
                                                        height=35, command=self.add_more_players_to_game_button_event)
        add_more_players_to_game_button.grid(row=1, column=0, padx=10, pady=10)
        delete_player_from_game_button = ctk.CTkButton(self.home_buttons_frame, text="", fg_color="#BF2A2A",
                                                       hover_color="darkred", image=icons.Delete, height=35,
                                                       command=self.delete_player_from_game_button_event)
        delete_player_from_game_button.grid(row=1, column=1, padx=10, pady=10)
        duplicate_last_game_button = ctk.CTkButton(self.home_buttons_frame, text="", fg_color="#27219E",
                                                   hover_color="darkblue", image=icons.Duplicate, height=35,
                                                   command=self.duplicate_last_game_button_event)
        duplicate_last_game_button.grid(row=1, column=2, padx=10, pady=10)

        add_player_one_option_menu = ctk.CTkOptionMenu(self.home_buttons_frame, values=self.potential_players,
                                                       width=200, height=50, text_color="black")
        add_player_one_option_menu.grid(row=2, column=1, padx=5, pady=5)
        add_player_two_option_menu = ctk.CTkOptionMenu(self.home_buttons_frame, values=self.potential_players,
                                                       width=200, height=50, text_color="black")
        if len(self.potential_players) > 1:
            add_player_two_option_menu.set(self.potential_players[1])
        add_player_two_option_menu.grid(row=3, column=1, padx=5, pady=5)
        add_player_three_option_menu = ctk.CTkOptionMenu(self.home_buttons_frame, values=self.potential_players,
                                                         width=200, height=50, text_color="black")
        if len(self.potential_players) > 2:
            add_player_three_option_menu.set(self.potential_players[2])
        add_player_three_option_menu.grid(row=4, column=1, padx=5, pady=5)

        for x in [add_player_one_option_menu, add_player_two_option_menu, add_player_three_option_menu]:
            self._active_player_menus_list.append(x)

        save_game_button = ctk.CTkButton(self.home_buttons_frame, text="", fg_color="green",
                                         hover_color="darkgreen", image=icons.Save, height=35,
                                         font=ctk.CTkFont(size=20), command=self.save_new_game_button_event)
        save_game_button.grid(row=9, column=1, padx=20, pady=20)

    # home buttons frame button events
    def add_more_players_to_game_button_event(self) -> None:
        """
        Event for the add more players to game button in the home frame,
        adds a new player option menu to the game frame, up to 7 players but not less than 3

        :return: None
        """
        if len(self._active_player_menus_list) < 7:
            new_player_option_menu = ctk.CTkOptionMenu(self.home_buttons_frame, values=self.potential_players,
                                                       width=200, height=50, text_color="black")
            new_player_option_menu.grid(row=len(self._active_player_menus_list) + 2, column=1, padx=5, pady=5)
            self._active_player_menus_list.append(new_player_option_menu)

    def delete_player_from_game_button_event(self) -> None:
        """
        Event for the delete player from game button in the home frame,
        deletes player option menu from the game frame, but not less than 3 players

        :return: None
        """
        if len(self._active_player_menus_list) > 3:
            self._active_player_menus_list[-1].destroy()
            self._active_player_menus_list.pop()

    def duplicate_last_game_button_event(self) -> None:
        """
        Event for the duplicate last game button in the home frame,
        duplicates last used player line-up for the new game if it exists in the instance, or displays an error message

        :return: None
        """
        if self._last_game:
            while len(self._last_game) > len(self._active_player_menus_list):
                self.add_more_players_to_game_button_event()
            for index, player in enumerate(self._last_game):
                self._active_player_menus_list[index].set(player)
        else:
            error_entry = ctk.CTkEntry(self.home_buttons_frame, font=ctk.CTkFont(size=20), fg_color="transparent",
                                       border_width=5, border_color="#BF2A2A", width=250, height=50)
            error_entry.insert(0, "No last game to duplicate")
            error_entry.configure(state="disabled", justify="center")
            error_entry.grid(row=11, column=1, padx=20, pady=20)
            error_entry.after(1500, error_entry.destroy)

    def save_new_game_button_event(self) -> None:
        """
        Event for the save new game button in the home frame,
        saves the game to the database or displays an error message

        :return: None
        """
        players = []
        for player_menu in self._active_player_menus_list:
            players.append(player_menu.get())

        if len(players) != len(set(players)):
            error_entry = ctk.CTkEntry(self.home_buttons_frame, font=ctk.CTkFont(size=20), fg_color="transparent",
                                       border_width=5, border_color="#BF2A2A", width=250, height=50)
            error_entry.insert(0, "Players must be unique")
            error_entry.configure(state="disabled", justify="center")
            error_entry.grid(row=11, column=1, padx=20, pady=20)
            error_entry.after(1500, error_entry.destroy)
            return

        result = CRUD.create_game()
        self._latest_game_id = result
        if result:
            self._last_game = players
            success_entry = ctk.CTkEntry(self.home_buttons_frame, font=ctk.CTkFont(size=20), fg_color="transparent",
                                         border_width=5, border_color="green", width=250, height=50)
            success_entry.insert(0, f"Game added successfully")
            success_entry.configure(state="disabled", justify="center")
            success_entry.grid(row=11, column=1, padx=20, pady=20)
            success_entry.after(1500, success_entry.destroy)
            self._empty_game_present_flag = True
            self.controller.show_frame("TempGameFrame")
        elif result is False:
            CTkMessagebox(title="Warning", message=f"Error while adding game {players}", icon="warning",
                          corner_radius=10, sound=True, justify="center")
        else:
            # if result is None (no connection to database) shutdown the app
            self.quit()
