import customtkinter as ctk
from DB import CRUD
from CTkMessagebox import CTkMessagebox


class PlayersFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self._players = CRUD.get_all_users()

        self._players_labels = []
        self._players_edit_buttons = []
        self._players_delete_buttons = []

        self.grid_columnconfigure(0, weight=1)
        self.configure(label_text=f"Players count: {len(self._players) if len(self._players) > 0 else 0}",
                       label_text_color="black")

        for index, player in enumerate(self._players):
            player_label = ctk.CTkLabel(self, text=player[0], text_color="black", font=ctk.CTkFont(size=20),
                                        fg_color="grey50", corner_radius=20)
            player_label.grid(row=index + 1, column=0, padx=10, pady=10)
            self._players_labels.append(player_label)
            player_edit_button = ctk.CTkButton(self, text="", fg_color="#27219E",
                                               hover_color="darkblue", corner_radius=20,
                                               image=self.edit_image,
                                               command=lambda button_index=index:
                                               self.edit_player_button_event(button_index))
            player_edit_button.grid(row=index + 1, column=1, padx=(50, 5), pady=10)
            self._players_edit_buttons.append(player_edit_button)
            player_delete_button = ctk.CTkButton(self, text="", fg_color="#BF2A2A",
                                                 hover_color="darkred", corner_radius=20,
                                                 image=self.delete_image,
                                                 command=lambda button_index=index:
                                                 self.delete_player_button_event(button_index))
            player_delete_button.grid(row=index + 1, column=2, padx=(5, 20), pady=10)
            self._players_delete_buttons.append(player_delete_button)

# players frame button events
    def edit_player_button_event(self, index) -> None:
        """
        Event for the edit player button in the players frame,
        opens player editing window

        :param index: index of the player in the players list
        :return: None
        """
        if self._player_editing_flag:
            CTkMessagebox(title="Warning", message="You are already editing a player", icon="warning",
                          corner_radius=10, sound=True, justify="center")
            return
        else:
            self._player_editing_flag = True

        self._players_labels[index].destroy()
        self._players_edit_buttons[index].destroy()
        self._players_delete_buttons[index].destroy()

        new_name_entry = ctk.CTkEntry(self.players_list_frame, font=ctk.CTkFont(size=20), fg_color="transparent",
                                      border_width=3, border_color="lightblue", width=200, height=20)
        new_name_entry.grid(row=index + 1, column=0, padx=10, pady=10)
        save_new_name_button = ctk.CTkButton(self.players_list_frame, text="", fg_color="green",
                                             hover_color="darkgreen", image=self.save_image, corner_radius=20,
                                             command=lambda: self.save_new_name_button_event([self._players[index][0],
                                                                                              new_name_entry.get()]))
        save_new_name_button.grid(row=index + 1, column=1, padx=(50, 5), pady=10)
        cancel_player_edit_button = ctk.CTkButton(self.players_list_frame, text="", fg_color="#BF2A2A",
                                                  hover_color="darkred", image=self.cancel_image, corner_radius=20,
                                                  command=self.cancel_player_edit_button_event)
        cancel_player_edit_button.grid(row=index + 1, column=2, padx=(5, 20), pady=10)

    def delete_player_button_event(self, index) -> None:
        """
        Event for the delete player button in the players frame,
        deletes player from the database, or displays an error message

        :param index: index of the player in the players list
        :return: none
        """
        player_name = self._players[index][0]
        result = CRUD.delete_user(player_name)
        if result:
            # update players list for correct players list frame display
            self._players = CRUD.get_all_users()
            self.players_button_event()
        elif result is False:
            CTkMessagebox(title="Warning", message=f"Error while deleting user {player_name}", icon="warning",
                          corner_radius=10, sound=True, justify="center")
        else:
            # if result is None (no connection to database) shutdown the app
            self.quit()

    def save_new_name_button_event(self, editing_values: list) -> None:
        """
        Event for the save new name button in the players frame,
        saves the new player name to the database or displays an error message

        :param editing_values:
        :return:
        """
        result = CRUD.edit_user(editing_values[0], editing_values[1])

        if result:
            # update players list for correct players list frame display
            self._players = CRUD.get_all_users()
            self.players_button_event()
        elif result is False:
            CTkMessagebox(title="Warning", message=f"Error while editing user {editing_values[0]}", icon="warning",
                          corner_radius=10, sound=True, justify="center")
        else:
            # if result is None (no connection to database) shutdown the app
            self.quit()

    def cancel_player_edit_button_event(self) -> None:
        """
        Event for the cancel player edit button in the players frame,
        cancels the player editing and displays the player name

        :return: None
        """
        self.players_button_event()