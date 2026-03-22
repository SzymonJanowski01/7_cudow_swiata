import sqlite3

DATABASE_URL = r"D:\GITHUBDesktop\7_cudow_swiata\DB\7_cudow_baza.db"
TEST_DATABASE_URL = r"D:\GITHUBDesktop\7_cudow_swiata\DB\7_cudow_baza_test.db"

TESTING = False


def database_connect() -> sqlite3.Connection | None:
    """
    Establishes connection to the database
    :return: SQLite connection object
    """
    try:
        if not TESTING:
            sqlite_connection = sqlite3.connect(DATABASE_URL)
        else:
            sqlite_connection = sqlite3.connect(TEST_DATABASE_URL)

        return sqlite_connection

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        return None


def get_connection():
    """
    Provides connection object for interacting with the database
    :return: SQLite connection object
    """
    connection = database_connect()

    return connection


def clear_database() -> None:
    """
    Clears the database
    :return: None
    """
    with get_connection() as conn:
        try:
            cursor = conn.cursor()

            cursor.execute(
                f"DELETE FROM Users"
            )
            cursor.execute(
                f"DELETE FROM Games"
            )
            cursor.execute(
                f"DELETE FROM GameParticipant"
            )

            conn.commit()

        except sqlite3.Error as error:
            print("Error while clearing database", error)
