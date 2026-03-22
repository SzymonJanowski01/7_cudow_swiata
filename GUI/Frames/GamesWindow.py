import customtkinter as ctk
from DB import CRUD
from CTkMessagebox import CTkMessagebox


class GamesFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    games_number = len(self._games) if len(self._games) > 0 else 0
    self.games_list_frame = ctk.CTkScrollableFrame(self, corner_radius=50, fg_color="transparent",
                                                   label_text=f"Games: {games_number}",
                                                   label_font=ctk.CTkFont(size=35),
                                                   label_fg_color="grey60")

    case
    "games":
    self._current_frame = "games"
    self.games_list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    self.games_list_frame.configure(label_text=f"Games: {len(self._games)}", label_text_color="black")

    self.game_view_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
    self.game_view_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)  # type: ignore

    for index, game in enumerate(self._games):
        game_button = ctk.CTkButton(self.games_list_frame, text=game[1], text_color="black",
                                    font=ctk.CTkFont(size=20), fg_color="grey50", corner_radius=20,
                                    command=lambda game_index=index:
                                    self.view_game_button_event(game_index))
        game_button.grid(row=index + 1, column=0, padx=(0, 10), pady=10, sticky="nsew")

    if len(self._games) > 0:
        self.view_game_button_event(0)

    def view_game_button_event(self, index) -> None:
        """
        Event for the view game button in the games frame,
        opens game details window

        :param index: index of the game from the games list to display
        :return: none
        """
        self.clear_frame(self.game_view_frame)
        game_details = CRUD.get_game(self._games[index][0])  # type: ignore
        categories = ["Wonder", "Money", "Army", "Blue", "Yellow", "Green", "Purple", "Sum", "Rank"]
        firs_col_colors = ["grey50", "grey50", "#BF2A2A", "#27219E", "yellow", "green", "purple", "grey50", "grey50"]

        ranks = []
        for game in game_details:
            ranks.append(int(game[10]))

        rank_colors = sf.get_color_pattern(ranks)
        dense_ranks = ss.rankdata(ranks, method='dense').astype(int)  # type: ignore

        for row in range(0, 11):
            for col in range(len(game_details) + 1):
                if row == 0 and col == 0:
                    continue

                if row == 0:
                    label = ctk.CTkLabel(self.game_view_frame, text=CRUD.get_user_name(game_details[col-1][row]),
                                         font=ctk.CTkFont(size=20), text_color="black",
                                         fg_color="grey50", corner_radius=20)
                    label.grid(row=row, column=col, padx=5, pady=5)
                elif row == 1:
                    continue
                else:
                    if col == 0:
                        label = ctk.CTkLabel(self.game_view_frame, text=categories[row-2], height=30, width=90,
                                             font=ctk.CTkFont(size=20), text_color="black",
                                             fg_color=firs_col_colors[row-2], corner_radius=20)
                        label.grid(row=row-1, column=0, padx=10, pady=10)
                    else:
                        if row == 10:
                            label = ctk.CTkLabel(self.game_view_frame, text=str(game_details[col-1][row]),
                                                 text_color="black", font=ctk.CTkFont(size=20),
                                                 fg_color=rank_colors[dense_ranks[col-1]-1], corner_radius=20)
                            label.grid(row=row-1, column=col, padx=5, pady=5)
                        else:
                            label = ctk.CTkLabel(self.game_view_frame, text=str(game_details[col-1][row]),
                                                 text_color="black", font=ctk.CTkFont(size=20), fg_color="grey50",
                                                 corner_radius=20)
                            label.grid(row=row-1, column=col, padx=5, pady=5)

        delete_game_button = ctk.CTkButton(self.game_view_frame, text="", fg_color="#BF2A2A", hover_color="darkred",
                                           image=self.delete_image, corner_radius=20, width=50,
                                           command=lambda: self.delete_game_button_event(self._games[index][0]))
        delete_game_button.grid(row=11, column=(len(game_details) + 1) // 2, padx=10, pady=10)

    def delete_game_button_event(self, game_id) -> None:
        """
        Event for the delete game button in the games frame,
        deletes game from the database, or displays an error message

        :param game_id: id of the game to delete
        :return: none
        """
        result = CRUD.delete_game(game_id)
        if result:
            # update games list for correct games list frame display
            self._games = CRUD.get_all_games()
            self.games_button_event()
        elif result is False:
            CTkMessagebox(title="Warning", message=f"Error while deleting game {game_id}", icon="warning",
                          corner_radius=10, sound=True, justify="center")
        else:
            # if result is None (no connection to database) shutdown the app
            self.quit()