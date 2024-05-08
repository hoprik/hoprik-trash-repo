import json
import sqlite3


class SQL:
    def __init__(self):
        self.conn = sqlite3.connect('database.db', check_same_thread=False)
        self.create_table()

    def create_table(self):
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS users (user_id INT UNIQUE, symbols INT, blocks INT, tokens INT, token TEXT, messages TEXT)""")
        self.conn.commit()

    def create_user(self, user_id, token):
        start = json.dumps({"messages": []})
        self.conn.execute("""INSERT INTO users (user_id, symbols, blocks, tokens, token, messages) VALUES (?,?,?,?,?,?)""",
                          (user_id, 1000, 16, 10000, token, start))
        self.conn.commit()

    def update_user_id_by_token(self, user_id, token):
        self.conn.execute("""UPDATE users SET user_id = ? where token = ?""",
                          (user_id, token,))
        self.conn.commit()

    def get_user(self, user_id):
        cors = self.conn.execute("""SELECT * FROM users WHERE user_id = ?""", (user_id,))
        return cors.fetchone()

    def get_user_by_token(self, token) -> str:
        cors = self.conn.execute("""SELECT user_id FROM users WHERE token = ?""", (token,))
        return cors.fetchone()

    def get_symbols(self, user_id) -> int:
        cors = self.conn.execute("""SELECT symbols FROM users WHERE user_id = ?""", (user_id,))
        return cors.fetchone()[0]

    def get_blocks(self, user_id) -> int:
        cors = self.conn.execute("""SELECT blocks FROM users WHERE user_id = ?""", (user_id,))
        return cors.fetchone()[0]

    def get_tokens(self, user_id) -> int:
        cors = self.conn.execute("""SELECT tokens FROM users WHERE user_id = ?""", (user_id,))
        return cors.fetchone()[0]

    def get_messages(self, user_id) -> str:
        cors = self.conn.execute("""SELECT messages FROM users WHERE user_id = ?""", (user_id,))
        return cors.fetchone()[0]

    def take_away_symbols(self, user_id, symbols):
        self.conn.execute("""UPDATE users SET symbols = ? where user_id = ?""",
                          (self.get_symbols(user_id) - symbols, user_id,))
        self.conn.commit()

    def take_away_blocks(self, user_id, blocks):
        self.conn.execute("""UPDATE users SET blocks = ? where user_id = ?""",
                          (self.get_blocks(user_id) - blocks, user_id,))
        self.conn.commit()

    def take_away_tokens(self, user_id, token):
        self.conn.execute("""UPDATE users SET tokens = ? where user_id = ?""",
                          (self.get_tokens(user_id) - token, user_id,))
        self.conn.commit()

    def update_chat(self, user_id, messages):
        self.conn.execute("""UPDATE users SET messages = ? where user_id = ?""",
                          (messages, user_id,))
        self.conn.commit()
