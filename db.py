import sqlite3, json


class SQL:
    def __init__(self):
        self.conn = sqlite3.connect('manager.db')

    def create_user(self, id):
        story = {
            "user": "",
            "assistant": ""
        }
        self.conn.execute(
            """INSERT INTO account (user_id, tokens, season_id, gpt_history, genre, character, environment) VALUES (?,?,?,?,?,?,?)""",
            (id, 1000, 1, json.dumps(story), "", "", ""))

    def has_user(self, id):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * from account where id = ?""", id)
        rows = cursor.fetchall()
        return len(rows) != 0

    def count_users(self):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * from account""")
        rows = cursor.fetchall()
        return rows[-1]

    def set_genre(self, id, genre):
        cursor = self.conn.cursor()
        cursor.execute("""UPDATE account set level=? WHERE id = ?""", (genre, id))
        self.conn.commit()

    def set_character(self, id, character):
        cursor = self.conn.cursor()
        cursor.execute("""UPDATE account set character=? WHERE id = ?""", (character, id))
        self.conn.commit()

    def set_environment(self, id, environment):
        cursor = self.conn.cursor()
        cursor.execute("""UPDATE account set environment=? WHERE id = ?""", (environment, id))
        self.conn.commit()

    def set_gpt_history(self, id, text):
        cursor = self.conn.cursor()
        cursor.execute("""UPDATE account set gpt_history=? WHERE id = ?""", (text, id))
        self.conn.commit()

    def set_season(self, id, season_id):
        cursor = self.conn.cursor()
        cursor.execute("""UPDATE account set season_id=? WHERE id = ?""", (season_id, id))
        self.conn.commit()

    def set_tokens(self, id, tokens):
        cursor = self.conn.cursor()
        cursor.execute("""UPDATE account set tokens=? WHERE id = ?""", (tokens, id))
        self.conn.commit()

    def get_account(self, id):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * from account where id = ?""", id)
        rows = cursor.fetchall()
        return rows
