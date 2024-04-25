import sqlite3


class SQL:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.create_table()

    def create_table(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS users (user_id INT UNIQUE, symbols INT, blocks INT)""")
        self.conn.commit()

    def create_user(self, user_id):
        self.conn.execute("""INSERT INTO IF NOT EXISTS users (user_id, symbols, blocks) VALUES (?,?,?)""", (user_id, 1000, 16,))
        self.conn.commit()

    def get_tokens(self, user_id) -> int:
        cors = self.conn.execute("""SELECT symbols FROM users WHERE user_id=?""", user_id)
        return cors.fetchone()[0]

    def get_blocks(self, user_id) -> int:
        cors = self.conn.execute("""SELECT blocks FROM users WHERE user_id=?""", user_id)
        return cors.fetchone()[0]

    def take_away_symbols(self, user_id, symbols):
        self.conn.execute("""UPDATE users SET symbols=? where user_id=?""", (self.get_tokens(user_id)-symbols, user_id,))
        self.conn.commit()

    def take_away_blocks(self, user_id, blocks):
        self.conn.execute("""UPDATE users SET blocks=? where user_id=?""", (self.get_blocks(user_id)-blocks, user_id,))
        self.conn.commit()