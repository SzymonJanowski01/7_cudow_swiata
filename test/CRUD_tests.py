import random
import sqlite3
import pytest
from typing import List, Dict

from DB.CRUD import create_user, create_game, create_user_in_game
from DB.database import get_connection, clear_database

sample_users = ["user1", "user2", "user3", "user4"]


def test_create_user():
    create_user(random.choice(sample_users))

    with get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT UserID FROM Users"
            )
            result = cursor.fetchall()
            assert len(result) == 1
        except sqlite3.Error as error:
            print("Error while getting all users", error)

    clear_database()


def test_create_games():
    for _ in range(3):
        create_game()

    with get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT GameID FROM Games"
            )
            result = cursor.fetchall()
            assert len(result) == 3
        except sqlite3.Error as error:
            print("Error while getting all users", error)

    clear_database()


def test_create_user_in_game():
    users_ids = []
    game_ids = []


    for game_id in game_ids:
        for user_id in random.sample(users_ids, random.randint(3, 4)):
            create_user_in_game(game_id, {user_id: [random.randint(30, 80) for _ in range(8)]})


def get_user_scores(user_id: str) -> List[tuple] | None:
    with get_connection() as conn:
        try:
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT GameID, Score FROM GameParticipant WHERE UserID = ?",
                (user_id,)
            )
            result = cursor.fetchall()

            for i in range(len(result)):
                cursor.execute(
                    f"SELECT Date FROM Games WHERE GameID = ?",
                    (result[i][0],)
                )
                date = cursor.fetchone()
                result[i] = (result[i][0], result[i][1], date[0])

            return result

        except sqlite3.Error as error:
            print("Error while getting user scores", error)
            return


def get_multiple_user_scores(user_ids: List[str]) -> Dict[str, List[tuple]] | None:
    with get_connection() as conn:
        try:
            cursor = conn.cursor()

            result = {}
            for user_id in user_ids:
                cursor.execute(
                    f"SELECT GameID, Score FROM GameParticipant WHERE UserID = ?",
                    (user_id,)
                )
                result[user_id] = cursor.fetchall()

                for i in range(len(result[user_id])):
                    cursor.execute(
                        f"SELECT Date FROM Games WHERE GameID = ?",
                        (result[user_id][i][0],)
                    )
                    date = cursor.fetchone()
                    result[user_id][i] = (result[user_id][i][0], result[user_id][i][1], date[0])

            return result

        except sqlite3.Error as error:
            print("Error while getting multiple user scores", error)
            return
