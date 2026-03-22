from typing import List, Dict


class Game:
    def __init__(self, game_id: int, players_scores: Dict[int: List[int]]):
        self.game_id = game_id
        for x in range(len(players_scores) + 1, 8):
            players_scores[x] = [None, None, None, None, None, None, None, None, None]

        players_in_game = len(players_scores)
        for key, value in players_scores.items():
            pass


class User:
    def __init__(self, user_id: int, user_name: str):
        self.user_id = user_id
        self.user_name = user_name
