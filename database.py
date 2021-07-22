import os
import psycopg2
from config import Config

DB_URL = Config.DB_URL

class BotDatabase:
    def __init__(self, filename):
        self.conn = psycopg2.connect(DB_URL)

        self._add_users_table()
        self._add_api_key_table()

    def add_user(self, user_id, username):
        cursor = self.conn.cursor()
        sql_insert_query = '''INSERT INTO users (user_id, username) VALUES (%s, %s) ON CONFLICT DO NOTHING;'''
        sql_update_query = '''UPDATE users SET username = %s WHERE user_id = %s;'''
        cursor.execute(sql_insert_query, (user_id, username))
        cursor.execute(sql_update_query, (username, user_id))
        self.conn.commit()
        cursor.close()

    def add_api_key(self, user_id, api_key):
        cursor = self.conn.cursor()
        sql_query = '''INSERT INTO api_keys (user_id, api_key) VALUES (%s, %s) ON CONFLICT DO NOTHING;'''
        cursor.execute(sql_query, (user_id, api_key))
        self.conn.commit()
        cursor.close()

    def delete_api_key(self, user_id):
        cursor = self.conn.cursor()
        sql_query = '''DELETE FROM api_keys WHERE user_id = %s'''
        cursor.execute(sql_query, [user_id])
        self.conn.commit()
        cursor.close()

    def get_api_key(self, user_id):
        cursor = self.conn.cursor()
        sql_query = '''SELECT api_key FROM api_keys WHERE user_id=%s'''
        cursor.execute(sql_query, [user_id])
        key = cursor.fetchone()
        cursor.close()
        return key

    def get_all_users(self):
        cursor = self.conn.cursor()
        sql_query = '''SELECT user_id, username FROM users;'''
        cursor.execute(sql_query)
        records = cursor.fetchall()
        cursor.close()
        return records

    def update_user_username(self, user_id, new_username):
        cursor = self.conn.cursor()
        sql_update_query = '''UPDATE users SET username=%s WHERE user_id=%s;'''
        cursor.execute(sql_update_query, (new_username, user_id))
        self.conn.commit()
        cursor.close()

    def count_users(self):
        cursor = self.conn.cursor()
        sql_query = '''SELECT COUNT(user_id) FROM users;'''
        cursor.execute(sql_query)
        count = cursor.fetchone()
        cursor.close()
        return count

    def _add_users_table(self):
        cursor = self.conn.cursor()
        sql_query = '''CREATE TABLE IF NOT EXISTS 
                                    users (user_id BIGINT, username VARCHAR(64), PRIMARY KEY (user_id));'''
        cursor.execute(sql_query)
        self.conn.commit()
        cursor.close()

    def _add_api_key_table(self):
        cursor = self.conn.cursor()
        sql_query = '''CREATE TABLE IF NOT EXISTS api_keys (user_id BIGINT, api_key VARCHAR(100), PRIMARY KEY (user_id));'''
        cursor.execute(sql_query)
        self.conn.commit()
        cursor.close()

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    db = BotDatabase('bot_users.db')
    db.close()
