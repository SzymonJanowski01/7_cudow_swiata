import customtkinter as ctk
from DB import CRUD
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy.stats as ss


class StatsFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    self.stats_frame = ctk.CTkFrame(self, corner_radius=50, fg_color="transparent")

    self.stats_choices_frame = ctk.CTkScrollableFrame(self, corner_radius=50, fg_color="transparent",
                                                      border_color="grey50", border_width=2)

    case
    "stats":
    self._current_frame = "stats"
    self.stats_frame.grid(row=0, column=1, sticky="nsew")
    self.stats_frame.grid_rowconfigure((0, 1), weight=1)  # type: ignore

    self.stats_choices_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

    player_to_graph_button = ctk.CTkButton(self.stats_frame, text="Player graph", compound="top",
                                           height=200, width=200, image=self.user_image,
                                           text_color="black", font=ctk.CTkFont(size=20),
                                           command=self.select_player_to_graph_button_event)
    player_to_graph_button.grid(row=0, column=0, padx=20, pady=20)
    players_to_graph_button = ctk.CTkButton(self.stats_frame, text="Players graph", compound="top",
                                            height=200, width=200, image=self.users_image,
                                            text_color="black", font=ctk.CTkFont(size=20),
                                            command=self.select_players_to_graph_button_event)
    players_to_graph_button.grid(row=1, column=0, padx=20, pady=20)

    self.select_player_to_graph_button_event()

    def select_player_to_graph_button_event(self) -> None:
        """
        Event for the select player to graph button in the stats frame,
        creates a window for selecting player and stats to graph

        :return: None
        """
        self.clear_frame(self.stats_choices_frame)
        self._player_chekboxes = []
        self.stats_choices_frame.grid_rowconfigure(7, weight=1)  # type: ignore
        self.stats_choices_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)  # type: ignore

        information_label = ctk.CTkLabel(self.stats_choices_frame, text="*Scores are always selected by default*",
                                         font=ctk.CTkFont(size=16), fg_color="transparent")
        information_label.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

        selection_label = ctk.CTkLabel(self.stats_choices_frame, text="Select player to graph:",
                                       font=ctk.CTkFont(size=20), fg_color="transparent")
        selection_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        player_to_graph_option_menu = ctk.CTkOptionMenu(self.stats_choices_frame,
                                                        values=[player[0] for player in self._players],
                                                        width=200, height=50, text_color="black")
        player_to_graph_option_menu.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

        wonder_checkbox = ctk.CTkCheckBox(self.stats_choices_frame, text="Wonder", onvalue="on", offvalue="off",
                                          font=ctk.CTkFont(size=20))
        wonder_checkbox.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        self._player_chekboxes.append(wonder_checkbox)
        money_checkbox = ctk.CTkCheckBox(self.stats_choices_frame, text="Money", onvalue="on", offvalue="off",
                                         font=ctk.CTkFont(size=20))
        money_checkbox.grid(row=3, column=2, columnspan=2, padx=10, pady=10)
        self._player_chekboxes.append(money_checkbox)
        army_checkbox = ctk.CTkCheckBox(self.stats_choices_frame, text="Army", onvalue="on", offvalue="off",
                                        font=ctk.CTkFont(size=20))
        army_checkbox.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        self._player_chekboxes.append(army_checkbox)
        blue_checkbox = ctk.CTkCheckBox(self.stats_choices_frame, text="Blue", onvalue="on", offvalue="off",
                                        font=ctk.CTkFont(size=20))
        blue_checkbox.grid(row=4, column=2, columnspan=2, padx=10, pady=10)
        self._player_chekboxes.append(blue_checkbox)
        yellow_checkbox = ctk.CTkCheckBox(self.stats_choices_frame, text="Yellow", onvalue="on", offvalue="off",
                                          font=ctk.CTkFont(size=20))
        yellow_checkbox.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
        self._player_chekboxes.append(yellow_checkbox)
        green_checkbox = ctk.CTkCheckBox(self.stats_choices_frame, text="Green", onvalue="on", offvalue="off",
                                         font=ctk.CTkFont(size=20))
        green_checkbox.grid(row=5, column=2, columnspan=2, padx=10, pady=10)
        self._player_chekboxes.append(green_checkbox)
        purple_checkbox = ctk.CTkCheckBox(self.stats_choices_frame, text="Purple", onvalue="on", offvalue="off",
                                          font=ctk.CTkFont(size=20))
        purple_checkbox.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
        self._player_chekboxes.append(purple_checkbox)
        position_checkbox = ctk.CTkCheckBox(self.stats_choices_frame, text="Position", onvalue="on", offvalue="off",
                                            font=ctk.CTkFont(size=20))
        position_checkbox.grid(row=6, column=2, columnspan=2, padx=10, pady=10)
        self._player_chekboxes.append(position_checkbox)

        show_player_graph_button = ctk.CTkButton(self.stats_choices_frame, text="", height=20, width=200,
                                                 image=self.view_image, fg_color="#27219E", hover_color="darkblue",
                                                 command=lambda:
                                                 self.show_player_graph_button_event(player_to_graph_option_menu.get()))
        show_player_graph_button.grid(row=9, column=0, columnspan=5, padx=10, pady=10)

    def select_players_to_graph_button_event(self) -> None:
        """
        Event for the select players to graph button in the stats frame,
        creates a window for selecting players to graph their scores

        :return: None
        """
        self.clear_frame(self.stats_choices_frame)
        self.stats_choices_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)  # type: ignore
        for index in range((len(self._players) // 4) + 1):
            self.stats_choices_frame.grid_rowconfigure(index, weight=1)
        self._players_chekboxes = []

        show_players_graphs_button = ctk.CTkButton(self.stats_choices_frame, text="", height=20, width=200,
                                                   image=self.view_image, fg_color="#27219E", hover_color="darkblue",
                                                   command=self.show_players_graph_button_event)
        show_players_graphs_button.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

        for index, player in enumerate(self._players):
            player_label = ctk.CTkLabel(self.stats_choices_frame, text=player[0], font=ctk.CTkFont(size=20),
                                        fg_color="transparent", corner_radius=20)
            player_label.grid(row=int((index // 1.9) + 1), column=int((index % 2) * 2), padx=10, pady=10)
            player_checkbox = ctk.CTkCheckBox(self.stats_choices_frame, text="", onvalue="on", offvalue="off")
            player_checkbox.grid(row=int((index // 1.9) + 1), column=int((index % 2) * 2 + 1), padx=10, pady=10)
            self._players_chekboxes.append(player_checkbox)

    def show_player_graph_button_event(self, player_name) -> None:
        """
        Event for the show player graph button in the stats frame,
        creates a graph of the player scores for selected stats

        :param player_name: Name of the player to graph
        :return: None
        """
        fields_to_graph = []
        for box in self._player_chekboxes:
            if box.get() == "on":
                fields_to_graph.append(box.cget('text'))

        player_id = CRUD.get_user_id(player_name)
        if not player_id:
            CTkMessagebox(title="Warning", message="No such player", icon="warning", corner_radius=10,
                          sound=True, justify="center")
            return

        player_data = CRUD.get_user_scores(player_id, fields_to_graph)

        if player_data[0]:
            names = player_data[0]
            values = player_data[1]
            dates = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M") for date in names]

            y_dim = 0
            x_dim = 0
            for number in range(len(player_data[1])):
                if y_dim * x_dim >= len(player_data[1]):
                    break
                if number % 2 == 0:
                    x_dim += 1
                else:
                    y_dim += 1

            # displaying one graph
            if x_dim + y_dim == 1:
                fig, ax = plt.subplots(figsize=(7, 7))

                ax.xaxis.set_major_formatter(mdates.DateFormatter("%y-%m-%d"))
                ax.xaxis.set_major_locator(mdates.DayLocator())

                ax.set_xticks(dates)
                ax.xaxis_date()
                ax.tick_params(axis="x", rotation=335)
                ax.set_title(f"{player_name} Scores")
                ax.set_xlabel("Dates")
                ax.set_ylabel(f"Scores")
                ax.grid(True)

                # cursor = mplcursors.cursor(lines, hover=True)
                # cursor.connect("add", lambda sel: sel.annotation.set_text(
                #     f"{mdates.num2date(sel.target[0]).strftime('%y-%m-%d %H:%M')}\nScore: {int(sel.target[1])}"
                # ))

            # displaying two graphs
            elif x_dim + y_dim == 2:
                fig, axes = plt.subplots(1, 2, figsize=(10, 5))

                dict_keys = list(player_data[1].keys())

                for i, ax in enumerate(axes):
                    metric = dict_keys[i]
                    ax.plot(dates, values[metric], color="blue", marker="o")
                    ax.xaxis.set_major_formatter(mdates.DateFormatter("%y-%m-%d"))
                    ax.xaxis.set_major_locator(mdates.DayLocator())
                    ax.set_xticks(dates)
                    ax.tick_params(axis="x", rotation=335)

                    ax.set_title(f"{player_name} {metric}")
                    ax.set_xlabel("Dates")
                    ax.set_ylabel(metric)
                    ax.grid(True)

                fig.align_labels()
                fig.align_titles()

            # displaying three or more graphs
            else:
                if x_dim + y_dim == 3:
                    x_dim = 2
                    y_dim = 2

                if x_dim + y_dim == 6:
                    size = (15, 10)
                else:
                    size = (10, 7)
                fig, axs = plt.subplots(x_dim, y_dim, layout="constrained", figsize=size)

                dict_key_index = 0
                dict_keys = list(player_data[1].keys())

                for x in range(x_dim):
                    for y in range(y_dim):
                        if dict_key_index >= len(dict_keys):
                            break
                        ax = axs[x, y] if x_dim > 1 else axs[y]

                        ax.plot(dates, values[dict_keys[dict_key_index]], color="blue", marker="o")
                        ax.xaxis.set_major_formatter(mdates.DateFormatter("%y-%m-%d"))
                        ax.xaxis.set_major_locator(mdates.DayLocator())
                        ax.set_xticks(dates)
                        ax.xaxis_date()
                        ax.tick_params(axis="x", rotation=335)
                        ax.set_title(f"{player_name} {dict_keys[dict_key_index]}")
                        ax.set_xlabel("Dates")
                        ax.set_ylabel(f"{dict_keys[dict_key_index]}")
                        ax.grid(True)

                        dict_key_index += 1
                fig.align_labels()
                fig.align_titles()

            plt.show()
        else:
            CTkMessagebox(title="Warning", message="No data for this player", icon="warning", corner_radius=10,
                          sound=True, justify="center")

    def show_players_graph_button_event(self) -> None:
        """
        Event for the show players graph button in the stats frame,
        creates a graph of the players scores for selected players

        :return: None
        """
        players_to_graph = []
        for index, box in enumerate(self._players_chekboxes):
            if box.get() == "on":
                players_to_graph.append(CRUD.get_user_id(self._players[index][0]))

        if not players_to_graph:
            CTkMessagebox(title="Warning", message="No players selected", icon="warning", corner_radius=10,
                          sound=True, justify="center")
            return

        data = CRUD.get_multiple_user_scores(players_to_graph)
        if not data[0]:
            CTkMessagebox(title="Warning", message="No data for selected players", icon="warning", corner_radius=10,
                          sound=True, justify="center")
            return
        dates, players_scores = data
        formatted_dates = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M") for date in dates]

        fig, ax = plt.subplots(figsize=(10, 7))

        for player in players_scores:
            ax.plot(formatted_dates, players_scores[player], marker="o", label=player)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%y-%m-%d"))
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.set_xticks(dates)

        ax.set_xlabel("Dates")
        ax.set_ylabel("Scores")
        ax.set_title("Players scores")

        ax.grid(True)
        ax.legend()

        plt.xticks(rotation=335)
        plt.show()