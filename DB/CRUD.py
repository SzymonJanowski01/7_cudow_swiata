import sqlite3
from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Tuple

from DB.database import get_connection


# additional functions
def check_tables() -> None:
    """
    Checks all tables in the database
    :return: None
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table';"
    )
    tables = cursor.fetchall()
    tables = [x[0] for x in tables]
    print(tables)


# User CRUD
def create_user(user_name: str) -> bool | None:
    """
    Creates a user in the database
    :param user_name: Name of the user, must be unique
    :return: True if user was created, False if user already exists or user_name is not between 1-10 characters, None if error occurred
    """
    if 1 > len(user_name) > 10:
        return False
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT * FROM Users"
            )
            result = cursor.fetchall()

            used_ids = [x[0] for x in result]
            used_names = [x[1] for x in result]

            while True:
                user_id = uuid4().hex
                if user_id not in used_ids:
                    break

            if user_name in used_names:
                return False

            cursor.execute(
                f"INSERT INTO Users (UserID, UserName) VALUES (?, ?)",
                (user_id, user_name)
            )

            conn.commit()
            return True

    except sqlite3.Error as error:
        print("Error while creating users", error)
        return None


def get_user_id(user_name: str) -> str | None:
    with get_connection() as conn:
        try:
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT UserID FROM Users WHERE UserName = ?",
                (user_name,)
            )
            result = cursor.fetchone()

            if not result:
                return None

            return result[0]

        except sqlite3.Error as error:
            print("Error while getting user id", error)
            return


def get_user_name(user_id: str) -> str | None:
    with get_connection() as conn:
        try:
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT UserName FROM Users WHERE UserID = ?",
                (user_id,)
            )
            result = cursor.fetchone()
            return result[0]

        except sqlite3.Error as error:
            print("Error while getting user name", error)
            return


def get_all_users() -> List[str] | None:
    """
    Gets all users from the database
    :return: List of all UserNames in the database, None if error occurred
    """
    try:
        with get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute(
                f"SELECT UserName FROM Users ORDER BY UserName ASC"
            )
            result = cursor.fetchall()
            return list(result)

    except sqlite3.Error as error:
        print("Error while getting all users", error)
        return


def edit_user(user_name: str, new_user_name: str) -> bool | None:
    """
    Edits a user in the database

    :param user_name: Name of the user to be edited
    :param new_user_name: New name of the user
    :return: True if user was edited, False if user does not exist, None if error occurred
    """
    if new_user_name == "":
        return False
    elif new_user_name == user_name:
        return False

    with get_connection() as conn:
        try:
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT * FROM Users WHERE UserName = ?",
                (user_name,)
            )
            result = cursor.fetchone()
            if not result:
                return False

            cursor.execute(
                f"SELECT * FROM Users WHERE UserName = ?",
                (new_user_name,)
            )
            result = cursor.fetchone()
            if result:
                return False

            cursor.execute(
                f"UPDATE Users SET UserName = ? WHERE UserName = ?",
                (new_user_name, user_name)
            )

            conn.commit()
            return True

        except sqlite3.Error as error:
            print("Error while updating user", error)
            return


def delete_user(user_name: str) -> bool:
    """
    Deletes a user from the database

    :param user_name: UserName of the user to be deleted
    :return: True if user was deleted, False if user does not exist
    """
    with get_connection() as conn:
        try:
            cursor = conn.cursor()

            cursor.execute(
                f"DELETE FROM Users WHERE UserName = ?",
                (user_name,)
            )

            conn.commit()
            return True

        except sqlite3.Error as error:
            print("Error while deleting user", error)
            return False


# Game CRUD
def create_game() -> str | None:
    with get_connection() as conn:
        try:
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT GameID FROM Games"
            )
            result = cursor.fetchall()

            while True:
                game_id = uuid4().hex
                if game_id not in result:
                    break

            today = datetime.today().strftime('%Y-%m-%d %H:%M')

            cursor.execute(
                f"INSERT INTO Games (GameID, Date) VALUES (?, ?)",
                (game_id, today)
            )

            conn.commit()
            return game_id

        except sqlite3.Error as error:
            print("Error while creating games", error)
            return


def get_game(game_id: str) -> List[Tuple[str]] | None:
    with get_connection() as conn:
        try:
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT * FROM GameParticipant WHERE GameID = ?",
                (game_id,)
            )
            result = cursor.fetchall()
            return result

        except sqlite3.Error as error:
            print("Error while getting game", error)
            return


def get_all_games() -> List[tuple] | None:
    with get_connection() as conn:
        try:
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT GameID, Date FROM Games ORDER BY Date DESC"
            )
            result = cursor.fetchall()
            return result

        except sqlite3.Error as error:
            print("Error while getting all games", error)
            return


def delete_last_game() -> bool:
    with get_connection() as conn:
        try:
            cursor = conn.cursor()

            cursor.execute(
                f"DELETE FROM Games WHERE GameID = (SELECT GameID FROM Games ORDER BY Date DESC LIMIT 1)"
            )

            conn.commit()
            return True

        except sqlite3.Error as error:
            print("Error while deleting last game", error)
            return False


def delete_game(game_id: str) -> bool:
    with get_connection() as conn:
        try:
            cursor = conn.cursor()

            cursor.execute(
                f"DELETE FROM GameParticipant WHERE GameID = ?",
                (game_id,)
            )

            cursor.execute(
                f"DELETE FROM Games WHERE GameID = ?",
                (game_id,)
            )

            conn.commit()
            return True

        except sqlite3.Error as error:
            print("Error while deleting game", error)


# GameParticipant CRUD
def create_user_in_game(game_id: str, users_in_game: Dict[str, List[int]]) -> bool | None:
    with get_connection() as conn:
        try:
            cursor = conn.cursor()

            for username, stats in users_in_game.items():
                user_id = get_user_id(username)

                cursor.execute(
                    f"INSERT INTO GameParticipant "
                    f"(UserID, GameID, Wonder, Money, Army, Blue, Yellow, Green, Purple, Score, Position) "
                    f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (user_id, game_id, *stats)
                )
                conn.commit()
            return True

        except sqlite3.Error as error:
            print("Error while creating user in game", error)
            return


def get_user_scores(user_id: str, requested_values: List[str] = None) -> Tuple[list, Dict[str, list]] | None:
    with get_connection() as conn:
        try:
            cursor = conn.cursor()

            return_dict = {}
            if requested_values is None or requested_values == []:
                requested_values = ["Score"]
            elif "Score" not in requested_values:
                requested_values.insert(0, "Score")

            fields = ""
            for field in requested_values:
                fields += ", " + field

            cursor.execute(
                f"SELECT GameID{fields} FROM GameParticipant WHERE UserID = ?",
                (user_id,)
            )
            result = cursor.fetchall()

            for i in range(len(result)):
                cursor.execute(
                    f"SELECT Date FROM Games WHERE GameID = ?",
                    (result[i][0],)
                )
                date = cursor.fetchone()
                result[i] = (date[0], ) + result[i][1:]

            dates = []
            for index, field in enumerate(requested_values):
                return_dict[field] = [value[index + 1] for value in result]

            for game in result:
                dates.append(game[0])

            final_result = (dates, return_dict)

            return final_result

        except sqlite3.Error as error:
            print("Error while getting user scores", error)
            return


def get_multiple_user_scores(user_ids: List[str]) -> Tuple[List[str], Dict[str, List[int | None]]] | None:
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

            if not result:
                return None

            # create a list of all unique dates
            dates = []
            for user in result.values():
                for game in user:
                    dates.append(game[2])
            dates = list(set(dates))
            dates.sort()

            scores = {}
            for user_id in user_ids:
                user_name = get_user_name(user_id)
                scores[user_name] = []
                game_index = 0

                for date in dates:
                    if date in [game[2] for game in result[user_id]]:
                        scores[user_name].append(result[user_id][game_index][1])
                        game_index += 1
                    else:
                        scores[user_name].append(None)

            final_result = (dates, scores)
            return final_result

        except sqlite3.Error as error:
            print("Error while getting multiple user scores", error)
            return
