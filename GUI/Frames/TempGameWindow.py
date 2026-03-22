import customtkinter as ctk
from DB import CRUD
from CTkMessagebox import CTkMessagebox


class TempGameFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    self.game_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
    self.game_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)  # type: ignore

    if len(self._players) < 3:
        self.add_player_button_event()
    else:
        self.add_game_button_event()

    self.game_view_frame = ctk.CTkFrame(self, corner_radius=50, fg_color="transparent", border_color="grey50",
                                        border_width=2)

    case
    "game":
    self._current_frame = "game"
    firs_col_colors = ["grey50", "grey50", "#BF2A2A", "#27219E", "yellow", "green", "purple", "grey50"]

    for x in range(len(self._last_game) + 1):
        self.game_frame.grid_columnconfigure(x, weight=1)

    self.game_button.grid(row=5, column=0, sticky="ew")
    self.game_frame.grid(row=0, column=1, columnspan=2, sticky="nsew")

    first_column_values = ["Wonder", "Money", "Army", "Blue", "Yellow", "Green", "Purple", "Sum"]
    self.game_detail_entries = [[] for _ in range(len(self._last_game))]

    # create a table for game details
    # ten rows because of player names in row 0, and final rank in 9, rest according to first_column_values
    for x in range(10):
        # if it's the first row, fill it with player names
        if x == 0:
            for player in self._last_game:
                player_entry = ctk.CTkEntry(self.game_frame, font=ctk.CTkFont(size=15),
                                            fg_color="transparent", border_width=3,
                                            border_color="lightblue", width=120, height=30)
                player_entry.insert(0, player)
                player_entry.configure(state="disabled", justify="center")
                # +1 in column to skip the 0x0 (corner) entry
                player_entry.grid(row=x, column=self._last_game.index(player) + 1)
        # otherwise fill it with game details
        else:
            for y in range(len(self._last_game) + 1):
                # skip the 9x0 (corner) entry
                if x == 9 and y == 0:
                    continue
                player_entry = ctk.CTkEntry(self.game_frame, font=ctk.CTkFont(size=15),
                                            fg_color="transparent", border_width=3, border_color="grey50",
                                            width=120, height=30)
                player_entry.configure(justify="center")
                player_entry.grid(row=x, column=y)
                # fill the first column with first_column_values as those are names of the game details
                if y == 0 and x != 9:
                    player_entry.insert(0, f"{first_column_values[x - 1]}")
                    player_entry.configure(state="disabled", justify="center",
                                           border_color=firs_col_colors[x - 1])
                # disable last two rows as they are score and rank rows and should be inaccessible for
                # editing by user
                elif x == 9 or x == 8 and y != 0:
                    player_entry.configure(state="disabled", justify="center")
                    self.game_detail_entries[y - 1].append(player_entry)
                else:
                    self.game_detail_entries[y - 1].append(player_entry)

    calculate_button = ctk.CTkButton(self.game_frame, text="", fg_color="#27219E",
                                     image=self.calculate_image, hover_color="darkblue",
                                     width=120, height=35, command=self.calculate_button_event)
    calculate_button.grid(row=10, column=int(len(self._last_game) // 2.1), sticky="ew", padx=5, pady=5)
    save_game_details_button = ctk.CTkButton(self.game_frame, text="", fg_color="green",
                                             image=self.save_image, hover_color="darkgreen",
                                             width=120, height=35,
                                             command=self.save_game_details_button_event)
    save_game_details_button.grid(row=10, column=int((len(self._last_game) // 2.1) + 1), sticky="ew",
                                  padx=5, pady=5)
    cancel_game_details_button = ctk.CTkButton(self.game_frame, text="", fg_color="#BF2A2A",
                                               image=self.cancel_image, hover_color="darkred",
                                               width=120, height=35,
                                               command=self.cancel_game_details_button_event)
    cancel_game_details_button.grid(row=10, column=int((len(self._last_game) // 2.1) + 2), sticky="ew",
                                    padx=5, pady=5)

    def calculate_button_event(self) -> None:
        """
        Event for the calculate button in the game details frame,
        calculates the sum of points for each player and ranks them,
        incorrect entries are marked and missing entries will be filled with 0

        :return: None
        """
        position_list = []

        # check if all necessary entries are filled and fill them with 0 if not
        for entry_list in self.game_detail_entries:
            for entry in entry_list:
                if entry.get() == "" and entry != entry_list[-1] and entry != entry_list[-2]:
                    entry.insert(0, "0")

        # calculate sum points for each player
        for entry_list in self.game_detail_entries:
            col_sum = 0
            for entry in entry_list:
                if entry != entry_list[-1] and entry != entry_list[-2]:
                    try:
                        col_sum += int(entry.get())
                    except ValueError:
                        entry.configure(border_color="#BF2A2A")
                        CTkMessagebox(title="Warning", message="All entries must be integers", icon="warning",
                                      corner_radius=10, sound=True, justify="center")
                        self._game_properly_calculated_flag = False
                        return
                    entry.configure(border_color="grey50")

            entry_list[-2].configure(state="normal")
            entry_list[-2].delete(0, "end")
            entry_list[-2].insert(0, str(col_sum))
            entry_list[-2].configure(state="disabled")
            position_list.append(col_sum)

        self._game_properly_calculated_flag = True

        # replace sum points with ranks, bigger number means better rank
        ranked_list = len(position_list) - ss.rankdata(position_list, method='max').astype(int) + 1  # type: ignore

        # prepare list of colors for each rank
        ranked_list_to_color = len(position_list) - ss.rankdata(position_list,   # type: ignore
                                                                method='dense').astype(int)
        ranked_list_to_color = [int(x - min(ranked_list_to_color)) for x in ranked_list_to_color]

        color_list = sf.get_color_pattern(ranked_list)

        # fill rank entries with calculated ranks
        for index, entry_list in enumerate(self.game_detail_entries):
            entry_list[-1].configure(state="normal", text_color="black")
            entry_list[-1].delete(0, "end")
            entry_list[-1].insert(0, str(ranked_list[index]))
            # insert position color
            entry_list[-1].configure(fg_color=color_list[ranked_list_to_color[index]],
                                     border_color=color_list[ranked_list_to_color[index]], state="disabled")

    def save_game_details_button_event(self) -> None:
        """
        Event for the save game details button in the game details frame,
        saves the game details to the database or displays an error message

        :return: None
        """
        if self._game_properly_calculated_flag:
            values_for_update = {}

            for index, entry_list in enumerate(self.game_detail_entries):
                values_for_update[self._last_game[index]] = [entry.get() for entry in entry_list]

            result = CRUD.create_user_in_game(self._latest_game_id, values_for_update)
            if not result:
                msg = CTkMessagebox(title="Warning", message="Error while saving game details", icon="warning",
                                    corner_radius=10, sound=True, justify="center", option_1="OK")
                if msg.get() == "OK":
                    self.home_button_event()
                return

            # update games list for correct games list frame display
            self._games = CRUD.get_all_games()

            # set empty game flag to False as game details are saved
            self._empty_game_present_flag = False

            msg = CTkMessagebox(title="Success", message="Game details saved successfully", icon="check",
                                corner_radius=10, justify="center", option_1="OK")
            if msg.get() == "OK":
                self.home_button_event()
        else:
            CTkMessagebox(title="Warning", message="Game details are not properly calculated", icon="warning",
                          corner_radius=10, sound=True, justify="center")

    def cancel_game_details_button_event(self):
        """
        Event for the cancel game details button in the game details frame,
        cancels the game details editing and displays the game details

        :return: None
        """
        self.home_button_event()